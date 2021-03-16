import json


from writer.lib.deserializer import Deserializer
from writer.model.http_check_result import HTTPCheckResult


class JSONToHTTPCheckResult(Deserializer):
    def loads(self, obj: str) -> HTTPCheckResult:
        parsed = json.loads(obj)

        return HTTPCheckResult(
            url=parsed['url'],
            response_time=parsed['response_time'],
            status_code=parsed.get('status_code'),
            re_match=parsed.get('re_match'),
            error=parsed.get('error')
        )
