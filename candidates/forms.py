
from django import forms
from .models import Candidate


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate

        fields = [
            "name",
            "email",
            "phone",
            "job",
            "resume",
        ]

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")

        if not resume:
            raise forms.ValidationError("Please upload a resume.")

        allowed_extensions = [".pdf", ".docx"]

        filename = resume.name.lower()

        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Resume size must be less than 5 MB."
            )

        return resume
