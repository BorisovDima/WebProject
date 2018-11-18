from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # http default
    # Empty for now (http->django views is added by default)
})