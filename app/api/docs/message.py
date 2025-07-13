from fastapi import status

message_send_responses = {
    status.HTTP_201_CREATED: {
        "description": "Сообщение успешно отправлено.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "sender_id": 2,
                    "receiver_id": 3,
                    "text": "Привет!",
                    "timestamp": "2024-05-01T12:00:00",
                    "from_me": True
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Пользователь не найден (UserNotFoundError)",
        "content": {
            "application/json": {
                "example": {"detail": "Пользователь не найден."}
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации входных данных.",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка валидации."}
            }
        }
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Внутренняя ошибка сервера (DatabaseError)",
        "content": {
            "application/json": {
                "example": {"detail": "Внутренняя ошибка сервера."}
            }
        }
    },
}

get_chats_responses_raw = {
    "200": {
        "description": "Список чатов пользователя.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "companion_login": "user2",
                        "companion_avatar_url": "https://example.com/avatar.png",
                        "last_message": "Привет!",
                        "last_message_time": "2024-05-01T12:00:00",
                        "from_me": True
                    }
                ]
            }
        }
    },
    "404": {
        "description": "Пользователь не найден (UserNotFoundError)",
        "content": {
            "application/json": {
                "example": {"detail": "Пользователь не найден."}
            }
        }
    },
    "500": {
        "description": "Внутренняя ошибка сервера (DatabaseError)",
        "content": {
            "application/json": {
                "example": {"detail": "Внутренняя ошибка сервера."}
            }
        }
    },
}
get_chats_responses = {
    200: get_chats_responses_raw["200"],
    404: get_chats_responses_raw["404"],
    500: get_chats_responses_raw["500"],
}
