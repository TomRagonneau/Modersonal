"""
Django customized context processors for modersonal project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/ref/templates/api/
"""


def info(request):
    """General information related to Modersonal project."""
    return {
        'author': __import__(__name__).__author__,
        'copyright': __import__(__name__).__copyright__,
        'license': __import__(__name__).__license__,
        'version': __import__(__name__).__version__,
    }
