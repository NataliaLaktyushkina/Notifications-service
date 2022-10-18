import logging

from consumer_services import send_email  # noqa: E402
from consumer_services.additonal_data import additional_info_for_email  # noqa: E402

logger = logging.getLogger(__name__)


def generate_email(routing_key: str, body_json: dict) -> None:
    payload = body_json['payload']
    for user in payload['users']:
        content = user['content']
        add_data = additional_info_for_email(
            routing_key, user['user']['user_id'], content,
        )
        if add_data:
            send_email.main(add_data['receivers'],
                            add_data['subject'],
                            add_data['title'],
                            add_data['template'],
                            add_data['text'])
        else:
            logger.warning(f'There is not additional '
                           f'data for routing key {routing_key}')
