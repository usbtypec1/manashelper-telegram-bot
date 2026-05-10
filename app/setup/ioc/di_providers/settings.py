from dishka import Provider, Scope, provide, from_context

from app.setup.config.settings import AppSettings, MongodbUri


class SettingsProvider(Provider):
    scope = Scope.APP

    settings = from_context(AppSettings)

    @provide
    def provide_mongodb_url(self, settings: AppSettings) -> MongodbUri:
        return MongodbUri(settings.mongodb_url)
