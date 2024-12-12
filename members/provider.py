from members.custom_provider import CustomOAuth2Provider


class GoogleProvider(CustomOAuth2Provider):
    id = "google"  # 프로바이더 ID
    name = "Google"  # 프로바이더 이름


# 기존 프로바이더 등록 코드
provider_classes = [GoogleProvider]
