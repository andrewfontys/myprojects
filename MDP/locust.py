from locust import HttpUser, between, task

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_webpage(self):
        self.client.get("http://aab9e1f7dcd894d25929b0444ab527b6-1372371802.eu-central-1.elb.amazonaws.com")

    @task
    def post_form_data(self):
        form_data = {
            'patientName': 'Tim Bob',
            'patientInfo': 'is very sick',
        }

        response = self.client.post("http://aab9e1f7dcd894d25929b0444ab527b6-1372371802.eu-central-1.elb.amazonaws.com", data=form_data)

        print(response.text)
