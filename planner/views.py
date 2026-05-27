import os

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from groq import Groq

from .models import CurriculumPlan


@require_http_methods(['GET'])
def home(request):
    return render(request, 'index.html')


@require_http_methods(['POST'])
def generate_curriculum(request):
    topic = request.POST.get('topic', '').strip()
    timeframe = request.POST.get('timeframe', '').strip()
    level = request.POST.get('level', '').strip()

    if not topic or not timeframe or not level:
        return redirect('home')

    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        context = {
            'topic': topic,
            'timeframe': timeframe,
            'level': level,
            'content': '<ul><li>Configuration error: GROQ_API_KEY is not set.</li></ul>',
        }
        return render(request, 'result.html', context, status=500)

    client = Groq(api_key=api_key)

    system_prompt = (
        'You are an expert curriculum designer. Provide a structured, professional '
        '[Timeframe]-week curriculum for [Topic] at a [Skill Level] level. '
        'Return the output as HTML <ul> and <li> tags for readability.'
    )

    user_prompt = (
        f'Topic: {topic}\n'
        f'Timeframe: {timeframe} weeks\n'
        f'Skill Level: {level}\n'
        'Create a week-by-week curriculum. Keep it concise and actionable.'
    )

    completion = client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
        temperature=0.7,
    )

    curriculum_html = completion.choices[0].message.content or '<ul><li>No curriculum generated.</li></ul>'

    plan = CurriculumPlan.objects.create(
        topic=topic,
        timeframe=int(timeframe),
        level=level,
        content=curriculum_html,
    )

    context = {
        'topic': plan.topic,
        'timeframe': plan.timeframe,
        'level': plan.level,
        'content': plan.content,
        'debug': settings.DEBUG,
    }
    return render(request, 'result.html', context)
