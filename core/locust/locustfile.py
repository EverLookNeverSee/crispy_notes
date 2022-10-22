from locust import HttpUser, task


class QuickstartUser(HttpUser):
    def on_start(self):
        response = self.client.post(
            url="/accounts/api/v2/jwt/create/",
            data={"email": "admin@admin.com", "password": "123456"},
        ).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access', None)}"
        }

    @task
    def get_user_profile(self):
        self.client.get("accounts/api/v2/profile/")

    @task
    def get_categories_list(self):
        self.client.get("/blog/api/v1/category/")

    @task
    def get_category_detail(self):
        self.client.get("/blog/api/v1/category/1")

    @task
    def get_posts_list(self):
        self.client.get("/blog/api/v1/post/")

    @task
    def get_post_detail(self):
        self.client.get("/blog/api/v1/post/1")

    @task
    def get_user_comments_list(self):
        self.client.get("comment/api/v1/comments/")
