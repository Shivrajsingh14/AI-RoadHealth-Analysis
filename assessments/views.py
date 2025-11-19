from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assessment
from .forms import AssessmentUploadForm
from ai.gemini_ai import analyze_road_condition
from django.conf import settings
import os


@login_required
def dashboard_view(request):
	assessments = Assessment.objects.filter(user=request.user)
	return render(request, 'assessments/dashboard.html', {'assessments': assessments})


@login_required
def upload_view(request):
	if request.method == 'POST':
		form = AssessmentUploadForm(request.POST, request.FILES)
		if form.is_valid():
			assessment = form.save(commit=False)
			assessment.user = request.user
			assessment.analysis_status = 'analyzing'
			assessment.save()
            
			# Analyze using Gemini
			image_path = os.path.join(settings.MEDIA_ROOT, assessment.image.name)
			result = analyze_road_condition(image_path)
			if result:
				assessment.crack_percentage = result.get('crack_percentage')
				assessment.pothole_probability = result.get('pothole_probability')
				assessment.severity = result.get('severity')
				assessment.condition_score = result.get('condition_score')
				assessment.analysis_status = 'completed'
			else:
				assessment.analysis_status = 'failed'
			assessment.save()
			return redirect('result', assessment_id=assessment.id)
	else:
		form = AssessmentUploadForm()
	return render(request, 'assessments/upload.html', {'form': form})


@login_required
def result_view(request, assessment_id):
	assessment = get_object_or_404(Assessment, id=assessment_id, user=request.user)
	return render(request, 'assessments/result.html', {'assessment': assessment})
