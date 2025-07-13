
comment_create_responses_raw = {
    "201": {
        "description": "Комментарий успешно создан.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 2,
                    "history_id": 3,
                    "content": "Комментарий",
                    "created_at": "2024-05-01T12:00:00",
                    "updated_at": None
                }
            }
        }
    },
    "422": {
        "description": "Ошибка валидации входных данных.",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка валидации."}
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
comment_create_responses = {
    201: comment_create_responses_raw["201"],
    422: comment_create_responses_raw["422"],
    500: comment_create_responses_raw["500"],
}

comment_get_responses_raw = {
    "200": {
        "description": "Комментарий найден.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 2,
                    "history_id": 3,
                    "content": "Комментарий",
                    "created_at": "2024-05-01T12:00:00",
                    "updated_at": None
                }
            }
        }
    },
    "404": {
        "description": "Комментарий не найден (CommentNotFoundError)",
        "content": {
            "application/json": {
                "example": {"detail": "Комментарий не найден."}
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
comment_get_responses = {
    200: comment_get_responses_raw["200"],
    404: comment_get_responses_raw["404"],
    500: comment_get_responses_raw["500"],
}

comment_update_responses_raw = {
    "200": {
        "description": "Комментарий успешно обновлён.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 2,
                    "history_id": 3,
                    "content": "Обновлённый комментарий",
                    "created_at": "2024-05-01T12:00:00",
                    "updated_at": "2024-05-02T12:00:00"
                }
            }
        }
    },
    "404": {
        "description": "Комментарий не найден (CommentNotFoundError)",
        "content": {
            "application/json": {
                "example": {"detail": "Комментарий не найден."}
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
comment_update_responses = {
    200: comment_update_responses_raw["200"],
    404: comment_update_responses_raw["404"],
    500: comment_update_responses_raw["500"],
}

comment_delete_responses_raw = {
    "204": {
        "description": "Комментарий успешно удалён.",
        "content": {
            "application/json": {
                "example": None
            }
        }
    },
    "404": {
        "description": "Комментарий не найден (CommentNotFoundError)",
        "content": {
            "application/json": {
                "example": {"detail": "Комментарий не найден."}
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
comment_delete_responses = {
    204: comment_delete_responses_raw["204"],
    404: comment_delete_responses_raw["404"],
    500: comment_delete_responses_raw["500"],
} 
