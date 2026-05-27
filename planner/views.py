from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from groq import Groq


@require_http_methods(['GET', 'POST'])
def curriculum_view(request):
    error = None

    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        timeframe = request.POST.get('timeframe', '').strip()
        level = request.POST.get('level', '').strip()

        if topic and timeframe and level:
            if not settings.GROQ_API_KEY:
                error = 'Server configuration error: GROQ_API_KEY is missing.'
            else:
                client = Groq(api_key=settings.GROQ_API_KEY)
                system_prompt = (
                    'You are an expert curriculum designer. Provide a structured, professional '
                    '[Timeframe]-week curriculum for [Topic] at a [Skill Level] level. '
                    'Return the output as clean HTML, using <h2> for weeks and <ul>/<li> for content.'
                )
                user_prompt = (
                    f'Topic: {topic}\n'
                    f'Timeframe: {timeframe} weeks\n'
                    f'Skill Level: {level}\n'
                    'Generate a concise, practical weekly curriculum.'
                )

                completion = client.chat.completions.create(
                    model='llama-3.1-8b-instant',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt},
                    ],
                    temperature=0.7,
                )
                curriculum = completion.choices[0].message.content or '<p>No curriculum generated.</p>'
                request.session['curriculum'] = curriculum
                request.session['form_data'] = {
                    'topic': topic,
                    'timeframe': timeframe,
                    'level': level,
                }
        else:
            error = 'Please fill in topic, timeframe, and skill level.'

    context = {
        'curriculum': request.session.get('curriculum'),
        'form_data': request.session.get('form_data', {}),
        'error': error,
    }
    return render(request, 'index.html', context)
