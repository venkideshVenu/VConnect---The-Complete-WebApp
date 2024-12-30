from django.contrib.auth.decorators import login_required
from .forms import RoleSelectionForm
from .forms import PayBalanceForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BikeShareProfile
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum, Count
from django.core import serializers
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Bike, Station, Order, BikeShareProfile
from .forms import TopUpForm, PayBalanceForm, LocationForm
import datetime
from .models import Station, Bike, Order, BikeShareProfile
import datetime
from django.db.models import Count, Q
from .forms import TopUpForm
from django.db import transaction


def index(request):
    # Get all stations for the locations section
    stations = Station.objects.all()

    # Get top stations by bike availability
    top_stations = Station.objects.annotate(
        available_bikes=Count(
            "bike_set", filter=Q(bike_set__in_use=False, bike_set__is_faulty=False)
        )
    ).order_by("-available_bikes")[:6]

    context = {
        "stations": stations,
        "top_stations": top_stations,
    }
    return render(request, "bikeshare/index.html", context)


def about(request):
    return render(request, "bikeshare/about.html")


@login_required
def select_role(request):
    """
    View to allow users to select their BikeShare role (Customer, Operator, or Manager).
    """
    try:
        profile = BikeShareProfile.objects.get(user=request.user)
        # Redirect if role is already selected
        if profile.role:
            return redirect(
                "bikeshare:bikeshare-customer"
                if profile.role == "Customer"
                else "bikeshare:bikeshare-operator"
                if profile.role == "Operator"
                else "bikeshare:bikeshare-manager"
            )
    except BikeShareProfile.DoesNotExist:
        profile = BikeShareProfile.objects.create(user=request.user)

    if request.method == "POST":
        role = request.POST.get("role")
        if role in ["Customer", "Operator", "Manager"]:
            profile.role = role
            profile.save()

            # Mark profile section as complete
            request.user.mark_profile_section_complete("bikeshare_profile", True)

            messages.success(request, f"Profile role set as {role}")

            # Redirect based on role
            if role == "Customer":
                return redirect("bikeshare:bikeshare-customer")
            elif role == "Operator":
                return redirect("bikeshare:bikeshare-operator")
            else:
                return redirect("bikeshare:bikeshare-manager")
        else:
            messages.error(request, "Invalid role selected")

    return render(request, "bikeshare/select_role.html")


def rent_bike(request, station_id):
    # Get station object from the ID
    station = get_object_or_404(Station, pk=station_id)
    # Get the first available bike
    bike = station.bike_set.all().filter(in_use=False, is_faulty=False).first()

    if not bike:
        return render(
            request,
            "bikeshare/customer_page.html",
            {
                "error": "No available bikes at this station.",
                "all_stations": Station.objects.all(),
                "all_bikes": Bike.objects.all(),
                "customers_orders": Order.objects.all(),
            },
        )

    rented_bike = get_object_or_404(Bike, pk=bike.id)

    # Get the user's BikeShareProfile
    try:
        user_profile = request.user.bikeshare_profile
    except BikeShareProfile.DoesNotExist:
        return render(
            request,
            "bikeshare/customer_page.html",
            {
                "error": "BikeShareProfile not found for this user.",
                "all_stations": Station.objects.all(),
                "all_bikes": Bike.objects.all(),
                "customers_orders": Order.objects.all(),
            },
        )

    # Start the rental process
    time = datetime.datetime.now()

    # Increment user's hires in progress
    user_profile.hires_in_progress += 1
    user_profile.save()

    # Create a new order
    new_order = Order(
        bike=rented_bike, user=request.user, start_station=station, start_time=time
    )
    new_order.save()

    # Mark the bike as in use
    rented_bike.in_use = True
    rented_bike.save()

    context = {
        "user": user_profile,
        "all_stations": Station.objects.all(),
        "all_bikes": Bike.objects.all(),
        "customers_orders": Order.objects.all(),
    }
    return render(request, "bikeshare/customer_page.html", context=context)


def submit_pay_balance(request):
    msg = ""

    if request.method == "POST":
        form = PayBalanceForm(request.POST)
        if form.is_valid():
            # Access the related `BikeShareProfile` instance
            user_profile = request.user.bikeshare_profile

            payment_amount = form.cleaned_data["money"]
            if (
                payment_amount <= user_profile.wallet_balance
                and payment_amount <= user_profile.amount_owed
            ):
                user_profile.wallet_balance -= payment_amount
                user_profile.amount_owed -= payment_amount
                user_profile.save()

                if user_profile.amount_owed == 0:
                    msg = "You have paid off all your balance!"
                else:
                    msg = "You have paid ₹{}. You still owe ₹{}".format(
                        payment_amount, user_profile.amount_owed
                    )
            elif payment_amount > user_profile.wallet_balance:
                msg = "You don't have enough money in your wallet."
            elif payment_amount > user_profile.amount_owed:
                msg = "You don't owe this much."

        context = {"msg": msg, "form": form}
        return render(request, "bikeshare/pay_balance.html", context=context)
    else:
        form = PayBalanceForm()
        return render(request, "bikeshare/pay_balance.html", {"form": form})


def submit_top_up(request):
    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = request.user.bikeshare_profile
                amount = form.cleaned_data["amount"]
                user.wallet_balance += float(amount)
                user.save()
                success_message = f"You have topped up by ₹{amount:.2f}"

                # Optional: Add a success message that can be displayed on redirect
                messages.success(request, success_message)

                # Optional: Redirect to customer page after successful top-up
                return redirect("bikeshare:bikeshare-customer")
        else:
            form = TopUpForm()

    context = {
        "form": form,
        "success_message": success_message if "success_message" in locals() else None,
    }
    return render(request, "bikeshare/top_up.html", context=context)


from django.conf import settings


@login_required
def customer_page(request):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if profile.role != "Customer":
        messages.error(
            request, "Access denied. You must be a customer to view this page."
        )
        return redirect("homepage")

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    customers_orders = Order.objects.filter(user=request.user)
    all_stations_map = serializers.serialize("json", Station.objects.all())

    context = {
        "profile": profile,
        "all_stations": all_stations,
        "all_bikes": all_bikes,
        "customers_orders": customers_orders,
        "form": LocationForm(),
        "all_stations_map": all_stations_map,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, "bikeshare/customer_page.html", context)


@login_required
def return_bike(request, order_id):
    profile = get_object_or_404(BikeShareProfile, user=request.user)
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            end_station = form.cleaned_data["locations"]
            end_time = timezone.now()

            # Calculate cost
            hours_used = (end_time - order.start_time).total_seconds() / 3600
            if hours_used <= 24:
                cost = (int(hours_used) + 1) * 5.00
            else:
                days = (end_time.date() - order.start_time.date()).days
                cost = 30.0 * days

            # Update order
            order.end_station = end_station
            order.check_out_time = end_time
            order.due_amount = cost
            order.is_complete = True
            order.save()

            # Update bike
            bike = order.bike
            bike.in_use = False
            bike.station = end_station
            bike.save()

            # Update user profile
            profile.hires_in_progress -= 1
            profile.amount_owed += cost
            profile.save()

            messages.success(
                request, f"Bike successfully returned. Amount charged: ₹{cost:.2f}"
            )
            return redirect("bikeshare:bikeshare-customer")
    else:
        form = LocationForm()

    context = {"form": form, "order": order, "profile": profile}
    return render(request, "bikeshare/return_bike.html", context)


@login_required
def top_up_balance(request):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["money"]
            profile.wallet_balance += amount
            profile.save()
            messages.success(request, f"Successfully topped up ₹{amount:.2f}")
            return redirect("bikeshare:bikeshare-customer")
    else:
        form = TopUpForm()

    return render(request, "bikeshare/top_up.html", {"form": form, "profile": profile})


@login_required
def pay_balance(request):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if request.method == "POST":
        form = PayBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["money"]
            if amount > profile.wallet_balance:
                messages.error(request, "Insufficient funds in wallet")
            elif amount > profile.amount_owed:
                messages.error(request, "Payment amount exceeds balance owed")
            else:
                profile.wallet_balance -= amount
                profile.amount_owed -= amount
                profile.save()
                messages.success(request, f"Successfully paid ₹{amount:.2f}")
                return redirect("bikeshare:bikeshare-customer")
    else:
        form = PayBalanceForm()

    return render(
        request, "bikeshare/pay_balance.html", {"form": form, "profile": profile}
    )


@login_required
def report_faulty(request, order_id):
    profile = get_object_or_404(BikeShareProfile, user=request.user)
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    order.fix_amount += 20.0
    order.save()

    profile.amount_owed += 15.00
    profile.save()

    bike = order.bike
    bike.is_faulty = True
    bike.save()

    messages.warning(request, "You have been charged ₹15 for reporting bike damage.")
    return redirect("bikeshare:bikeshare-customer")


@login_required
def operator_page(request):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if profile.role != "Operator":
        messages.error(
            request, "Access denied. You must be an operator to view this page."
        )
        return redirect("homepage")

    context = {
        "profile": profile,
        "faulty_bikes": Bike.objects.filter(is_faulty=True),
        "all_bikes": Bike.objects.all(),
        "move_stations": Station.objects.all(),
    }
    return render(request, "bikeshare/operator_page.html", context)


@login_required
def repair_bike(request, bike_id):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if profile.role != "Operator":
        messages.error(request, "Access denied. Only operators can repair bikes.")
        return redirect("homepage")

    bike = get_object_or_404(Bike, pk=bike_id)
    bike.is_faulty = False
    bike.save()

    messages.success(request, f"Bike {bike_id} has been repaired successfully.")
    return redirect("bikeshare:bikeshare-operator")


@login_required
def move_bike(request, bike_id):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if profile.role != "Operator":
        messages.error(request, "Access denied. Only operators can move bikes.")
        return redirect("homepage")

    bike = get_object_or_404(Bike, pk=bike_id)

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            new_station = form.cleaned_data["locations"]
            old_station = bike.station

            if new_station != old_station:
                bike.station = new_station
                bike.save()
                messages.success(
                    request, f"Bike moved from {old_station} to {new_station}"
                )
            else:
                messages.info(request, f"Bike is already at {new_station}")
            return redirect("bikeshare:bikeshare-operator")
    else:
        form = LocationForm()

    return render(
        request,
        "bikeshare/move_bike.html",
        {"form": form, "bike": bike, "profile": profile},
    )


@login_required
def manager_page(request):
    profile = get_object_or_404(BikeShareProfile, user=request.user)

    if profile.role != "Manager":
        messages.error(
            request, "Access denied. You must be a manager to view this page."
        )
        return redirect("homepage")

    # Profit per Station
    station_profit = None
    try:
        station_profits = (
            Order.objects.values("start_station__station_name")
            .annotate(profit=Sum("due_amount") - Sum("fix_amount"))
            .filter(profit__gt=0)
        )

        if station_profits:
            plt.clf()
            plt.title("Station Profit Distribution")
            plt.pie(
                [p["profit"] for p in station_profits],
                labels=[p["start_station__station_name"] for p in station_profits],
                autopct="%1.1f%%",
                shadow=True,
            )
            plt.axis("equal")
            buf = BytesIO()
            plt.savefig(buf, format="png")
            station_profit = base64.b64encode(buf.getvalue()).decode("utf-8")
            buf.close()
    except Exception as e:
        messages.error(request, f"Error generating profit chart: {str(e)}")

    # Route Frequency
    route_frequency = None
    try:
        routes = Order.objects.values(
            "start_station__station_name", "end_station__station_name"
        ).annotate(frequency=Count("id"))

        if routes:
            plt.clf()
            plt.figure(figsize=(10, 6))
            plt.title("Popular Routes")
            route_names = [
                f"{r['start_station__station_name']} → {r['end_station__station_name']}"
                for r in routes
                if r["end_station__station_name"]
            ]
            frequencies = [
                r["frequency"] for r in routes if r["end_station__station_name"]
            ]

            plt.barh(range(len(frequencies)), frequencies)
            plt.yticks(range(len(frequencies)), route_names)
            plt.xlabel("Number of Trips")

            buf = BytesIO()
            plt.savefig(buf, format="png")
            route_frequency = base64.b64encode(buf.getvalue()).decode("utf-8")
            buf.close()
    except Exception as e:
        messages.error(request, f"Error generating route chart: {str(e)}")

    # Top Users
    try:
        star_users = (
            Order.objects.values("user__username")
            .annotate(total_rides=Count("id"))
            .order_by("-total_rides")[:5]
        )
    except Exception as e:
        star_users = None
        messages.error(request, f"Error fetching top users: {str(e)}")

    context = {
        "profile": profile,
        "station_profit": station_profit,
        "route_frequency": route_frequency,
        "star_users": star_users,
    }
    return render(request, "bikeshare/manager_page.html", context)
