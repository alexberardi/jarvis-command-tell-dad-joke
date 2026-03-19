from typing import Any, List
from jarvis_command_sdk import (
    IJarvisCommand,
    CommandResponse,
    JarvisParameter,
    JarvisSecret,
    CommandExample,
    RequestInformation,
    JarvisPackage
)
import requests

try:
    from jarvis_log_client import JarvisLogger
except ImportError:
    import logging
    class JarvisLogger:
        def __init__(self, **kw): self._log = logging.getLogger(kw.get('service', __name__))
        def info(self, msg, **kw): self._log.info(msg)
        def warning(self, msg, **kw): self._log.warning(msg)
        def error(self, msg, **kw): self._log.error(msg)
        def debug(self, msg, **kw): self._log.debug(msg)


class TellDadJokeCommand(IJarvisCommand):
    def __init__(self):
        self.logger = JarvisLogger(service="tell_dad_joke")

    @property
    def command_name(self) -> str:
        return "tell_dad_joke"

    @property
    def description(self) -> str:
        return "Tells random dad jokes from icanhazdadjoke.com"

    @property
    def parameters(self) -> List[JarvisParameter]:
        return []

    @property
    def required_secrets(self) -> List[JarvisSecret]:
        return []

    @property
    def keywords(self) -> List[str]:
        return ["joke", "dad", "funny", "humor", "laugh", "comedy"]

    @property
    def required_packages(self) -> List[JarvisPackage]:
        return [JarvisPackage("requests", ">=2.28.0")]

    def generate_prompt_examples(self) -> List[CommandExample]:
        return [
            CommandExample(
                voice_command="tell me a joke",
                expected_parameters={},
                is_primary=True
            ),
            CommandExample(
                voice_command="I want to hear a dad joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="make me laugh",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="tell me something funny",
                expected_parameters={}
            )
        ]

    def generate_adapter_examples(self) -> List[CommandExample]:
        return [
            CommandExample(
                voice_command="tell me a joke",
                expected_parameters={},
                is_primary=True
            ),
            CommandExample(
                voice_command="I want to hear a dad joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="make me laugh",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="tell me something funny",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="give me a dad joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="I need a good joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="tell a joke please",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="can you tell me a joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="I could use a laugh",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="share a joke with me",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="tell me a corny joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="I want to hear something funny",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="make me smile with a joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="got any jokes for me",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="tell me your best dad joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="I'm in the mood for a joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="cheer me up with a joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="let me hear a joke",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="joke time",
                expected_parameters={}
            ),
            CommandExample(
                voice_command="tell me something that will make me laugh",
                expected_parameters={}
            )
        ]

    def run(self, request_info: RequestInformation, **kwargs: Any) -> CommandResponse:
        try:
            self.logger.info("Fetching dad joke from icanhazdadjoke.com")
            
            # Make request to icanhazdadjoke API
            headers = {
                "Accept": "application/json",
                "User-Agent": "Jarvis Assistant (https://github.com/jarvis-assistant)"
            }
            
            response = requests.get("https://icanhazdadjoke.com/", headers=headers, timeout=10)
            response.raise_for_status()
            
            joke_data = response.json()
            joke = joke_data.get("joke", "")
            
            if not joke:
                self.logger.warning("No joke found in API response")
                return CommandResponse.error_response(
                    "Sorry, I couldn't fetch a joke right now. Please try again later."
                )
            
            self.logger.info("Successfully fetched dad joke")
            
            return CommandResponse.final_response(
                context_data={
                    "message": joke,
                    "joke": joke,
                    "source": "icanhazdadjoke.com"
                }
            )
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch joke from API: {str(e)}")
            return CommandResponse.error_response(
                "Sorry, I'm having trouble connecting to the joke service. Please try again later."
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in tell_dad_joke: {str(e)}")
            return CommandResponse.error_response(
                "Sorry, something went wrong while trying to get a joke. Please try again."
            )