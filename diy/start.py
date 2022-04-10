from .. import BOT_SET
from ..user.login import user
if BOT_SET['开启user'].lower() == 'true':
    user.start()