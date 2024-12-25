from jobs.models import TagModel, JobModel, ApplicantModel
from jobprofile.models import Profile
from uuid import uuid4

# Assuming you have some profiles in the database
profiles = Profile.objects.all()

# Create Tags
tag1 = TagModel.objects.create(name="Python Developer")
tag2 = TagModel.objects.create(name="Remote Work")
tag3 = TagModel.objects.create(name="Full-time")
print("Tags created:", [tag1.name, tag2.name, tag3.name])

# Create Jobs
if profiles.exists():
    owner = profiles.first()  # Use the first profile as the job owner
    job1 = JobModel.objects.create(
        owner=owner,
        title="Junior Python Developer",
        description="Looking for a junior Python developer with knowledge of Django.",
        type="1",
        salary_range="₹30,000 - ₹50,000",
        location="Bangalore",
    )
    job1.tags.add(tag1, tag2)

    job2 = JobModel.objects.create(
        owner=owner,
        title="Remote React Developer",
        description="React Developer for a remote project.",
        type="2",
        salary_range="₹40,000 - ₹70,000",
        location="Remote",
    )
    job2.tags.add(tag2)

    print("Jobs created:", [job1.title, job2.title])

    # Create Applicants
    applicant1 = ApplicantModel.objects.create(
        user=profiles[1] if profiles.count() > 1 else owner,  # Use another profile if available
        job=job1,
        is_read=False,
        status='pending'
    )
    applicant2 = ApplicantModel.objects.create(
        user=owner,
        job=job2,
        is_read=True,
        status='reviewed'
    )

    print("Applicants created:", [str(applicant1), str(applicant2)])
else:
    print("No profiles available. Create some profiles first.")
