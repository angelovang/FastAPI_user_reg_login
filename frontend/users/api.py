from frontend.common.api import sync_request, API_URL
import requests

def register_user(username, email, password):
    return sync_request("POST", "/users/", {
        "username": username,
        "email": email,
        "password": password
    })


def get_users():
    try:
        response = requests.get(f"{API_URL}/users/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Грешка при зареждане на потребителите: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Грешка при заявката: {e}")
        return []


def update_user(user_id, username, email, role):
    return sync_request("PUT", f"/users/{user_id}", {
        "username": username,
        "email": email,
        "role": role
    })


def delete_user(user_id):
    return sync_request("DELETE", f"/users/{user_id}")


def change_password(user_id, old_password, new_password):
    try:
        response = sync_request(
            "PUT",
            f"/users/{user_id}/change-password",
            json={
                "old_password": old_password,
                "new_password": new_password
            }
        )

        return response
    except Exception as e:
        print(f"Грешка при смяна на паролата: {e}")
        return None
