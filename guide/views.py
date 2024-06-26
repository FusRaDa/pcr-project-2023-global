from django.shortcuts import render


def about_page(request):
  context = {}
  return render(request, 'about_page.html', context)


def faq_page(request):
  context = {}
  return render(request, 'faq_page.html', context)


def privacy_policy(request):
  context = {}
  return render(request, 'privacy_policy.html', context)


def subscription_policy(request):
  context = {}
  return render(request, 'subscription_policy.html', context)


def terms_conditions(request):
  context = {}
  return render(request, 'terms_conditions.html', context)


def email_opt_in(request):
  context = {}
  return render(request, 'email_opt_in.html', context)


def guide_page(request):
  context = {}
  return render(request, 'guide_page.html', context)


def inventory_guide(request):
  context = {}
  return render(request, 'guides/inventory_guide.html', context)


def tests_guide(request):
  context = {}
  return render(request, 'guides/tests_guide.html', context)


def protocols_guide(request):
  context = {}
  return render(request, 'guides/protocols_guide.html', context)


def extraction_guide(request):
  context = {}
  return render(request, 'guides/extraction_guide.html', context)


def pcr_guide(request):
  context = {}
  return render(request, 'guides/pcr_guide.html', context)


def articles_page(request):
  context = {}
  return render(request, 'articles_page.html', context)


def pcrmastermix_article(request):
  context = {}
  return render(request, 'articles/pcrmastermix.html', context)


