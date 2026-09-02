import subprocess
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def github_webhook_deploy(request):
    # Optional but recommended: Secure it with a secret query token
    secret_token = request.GET.get('token')
    if secret_token != "34b36454cab2e7842c389f7d88ecb7df279e3918cbac07970d4cde496e70f4c8":
        return HttpResponseForbidden("Unauthorized")

    if request.method == "POST":
        try:
            # Executes your local pull script right inside PythonAnywhere
            subprocess.run(["/home/ParkVenue/pull_and_migrate.sh"], check=True)
            return HttpResponse("Deployment Successful", status=200)
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Deployment Failed: {str(e)}", status=500)
            
    return HttpResponse("Method not allowed", status=405)
