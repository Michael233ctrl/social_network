import random
from random import randint
from time import perf_counter

import lorem
import names
import requests
from bot_config import MAX_LIKES_PER_USER as num_likes
from bot_config import MAX_POSTS_PER_USER as num_posts
from bot_config import NUMBER_OF_USERS as num_usrs
from bot_config import BACKEND_URL

token_list = []


def sign_up(username: str):
    """Register user and returns username.
    If username already exists, creates new by adding '_uno' to it."""
    response = requests.post(f'{BACKEND_URL}/api/v1/users/register/', json={
        'username': username,
        'password': 'somelongpass'
    })
    if response.status_code == 400:
        username = names.get_first_name()
        return sign_up(username)
    return username


def sign_in(username: str):
    """Log in user and save access token to token_list."""
    response = requests.post(f'{BACKEND_URL}/api/v1/users/login/',
                             data={'username': username,
                                   'password': 'somelongpass'})
    response = response.json()
    token_list.append(response.get('access'))


def post_create(token: str):
    """Create posts with random title and text."""
    random_title = lorem.sentence()
    random_text = lorem.paragraph()
    requests.post(f'{BACKEND_URL}/api/v1/posts/',
                  headers={'Content-Type': 'application/json',
                           'Authorization': f'Bearer {token}'},
                  json={
                        'title': f'{random_title}',
                        'body': f'{random_text}'
                    })


def post_like(post_id, token):
    requests.post(f'{BACKEND_URL}/api/v1/posts/{post_id}/like/',
                  headers={'Content-Type': 'application/json',
                           'Authorization': f'Bearer {token}'})


def main():
    """
    According to config_for_script.py file, create random users.
    Each user create random amount of posts, and then like or unlike them
    """
    for i in range(num_usrs):
        username = names.get_first_name()
        sign_in(sign_up(username))
        if token_list:
            token = token_list[i]
        for _ in range(randint(1, num_posts)):
            post_create(token)
        all_posts = requests.get(f"{BACKEND_URL}/api/v1/posts",
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {token}'})
        all_posts = all_posts.json()
        posts_id = [post['id'] for post in all_posts]
        for _ in range(randint(1, num_likes)):
            rand_post = random.choice(posts_id)
            post_like(rand_post, token)


if __name__ == '__main__':
    start = perf_counter()
    main()
    execution_time = perf_counter() - start
    print(f"Execution time: {execution_time:.4f} secs")
