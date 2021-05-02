from test_task_poll_app.models import Poll, Question, User, UserAnswer, Answer
from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def home(request, user_id):
    try:
        user_answers = list(UserAnswer.objects.all().filter(user_id=User.objects.get(site_id=user_id)))
        answered_polls = set()
        for user_answer in user_answers:
            answered_polls.add(user_answer.poll_id)
        all_polls = set(Poll.objects.all())
        not_answered_polls = all_polls - answered_polls
    except:
        p = User.objects.create(site_id=user_id)
        p.save()
        not_answered_polls = Poll.objects.all()
    return render(request, 'test_task_poll_app/home.html', {'pollItems': not_answered_polls, 'user_id': user_id})


def vote(request, user_id):
    poll_id = request.POST.get("poll_id", "")
    poll = Poll.objects.get(id=poll_id)
    questions = poll.questions.all()
    return render(request, 'test_task_poll_app/vote1.html', {'questions': questions, 'user_id': user_id})


def submit(request, user_id, poll_id):
    questions = list(Poll.objects.get(id=poll_id).questions.all())
    question_ids = []
    for question in questions:
        if question.type == '1':
            a = UserAnswer.objects.create(user_id=User.objects.get(site_id=user_id),
                                          answer_id=None,
                                          question_id=question,
                                          poll_id=Poll.objects.get(id=poll_id),
                                          text=request.POST.get(str(question.text)))
            a.save()
        elif question.type == '2':
            a = UserAnswer.objects.create(user_id=User.objects.get(site_id=user_id),
                                          answer_id=Answer.objects.get(id=request.POST.get(str(question.text))),
                                          question_id=question,
                                          poll_id=Poll.objects.get(id=poll_id))
            a.save()
        elif question.type == '3':
            for answer in list(question.pos_answers.all()):
                if request.POST.get(answer.choice_text) is not None:
                    a = UserAnswer.objects.create(user_id=User.objects.get(site_id=user_id),
                                                  answer_id=Answer.objects.get(id=request.POST.get(answer.choice_text)),
                                                  question_id=question,
                                                  poll_id=Poll.objects.get(id=poll_id))
                    a.save()
    return redirect('home', user_id=user_id)


def results_main(request, user_id):
    user_answers = list(UserAnswer.objects.all().filter(user_id=User.objects.get(site_id=user_id)))
    answered_polls = set()
    for user_answer in user_answers:
        answered_polls.add(user_answer.poll_id)
    return render(request, 'test_task_poll_app/results_main.html', {'pollItems': answered_polls, 'user_id': user_id})


def results(request, user_id):
    poll_id = request.POST.get("poll_id", "")
    poll = Poll.objects.get(id=poll_id)
    questions = poll.questions.all()
    questions_mass = []
    for question in questions:
        a = {'name': str(question.text), 'type': question.type}
        if question.type != '1':
            a['ans'] = []
            ua_for_q = UserAnswer.objects.all().filter(user_id=User.objects.get(site_id=user_id)).filter(
                poll_id=Poll.objects.get(id=poll_id)).filter(question_id=question)
            for x in question.pos_answers.all():
                b = {'name': x.choice_text, 'checked': ''}
                for y in ua_for_q:
                    if x == y.answer_id:
                        b['checked'] = 'checked'
                a['ans'].append(b)
        elif question.type == '1':
            a['ans'] = UserAnswer.objects.get(user_id=User.objects.get(site_id=user_id),
                                              poll_id=Poll.objects.get(id=poll_id), question_id=question).text
        questions_mass.append(a)
    return render(request, 'test_task_poll_app/results.html',
                  {'questions_mass': questions_mass, 'user_id': user_id, 'poll_name': poll.name})
