import logging

from consumer_services.additonal_data import additional_info_for_email  # noqa: E402
from consumer_services.auth_data import get_data_from_auth
from consumer_services.send_email import EmailSender  # noqa: E402

logger = logging.getLogger(__name__)


def generate_email(email_sender: EmailSender, routing_key: str, body_json: dict) -> None:
    payload: list = body_json['payload']
    for element in payload:
        for user in element['users']:
            user_data = get_data_from_auth(user)
            if user_data:
                content = element['content']
                add_data = additional_info_for_email(
                    routing_key, user_data, content,
                )
                if add_data:
                    email_sender.create_msg(
                        add_data['receivers'],
                        add_data['subject'],
                        add_data['title'],
                        add_data['template'],
                        add_data['text'],
                    )
                else:
                    logger.warning(f'There is not additional '
                                   f'data for routing key {routing_key}')
