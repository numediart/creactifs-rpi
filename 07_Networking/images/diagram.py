# /// script
# dependencies = [
#   "diagrams",
# ]
# ///


from diagrams import Cluster, Diagram, Edge
from diagrams.digitalocean.network import Domain
from diagrams.generic.compute import Rack
from diagrams.generic.device import Mobile
from diagrams.generic.network import VPN, Router, Switch
from diagrams.onprem.client import Client

graph_attr = {"pad": "1", "margin": "-1"}

with Diagram(
    "", filename="network", show=False, outformat="jpg", graph_attr=graph_attr
):
    with Cluster("Réseau local A"):
        local_1 = [
            Client("192.168.1.10"),
            Client("192.168.1.11"),
            Mobile("192.168.1.12"),
        ]

        router_1 = Router("Routeur")
        local_1 - router_1

    isp_1 = Switch("ISP")

    with Cluster("Réseau public", direction="TB", graph_attr={"style": "invis"}):
        dns = Rack("DNS\n1.1.1.1")
        internet = Domain("")
        server = Rack("raspberrypi.com\n172.67.154.53")

        dns - Edge(constraint="false") - internet
        internet - Edge(constraint="false") - server

    isp_2 = Switch("ISP")

    with Cluster("Réseau local B"):
        local_2 = [
            Client("192.168.1.11"),
            Mobile("192.168.1.10"),
            Client("192.168.1.9"),
        ]

        router_2 = Router("Routeur")
        router_2 - local_2

    router_1 - Edge(minlen="1.5") - isp_1 - Edge(minlen="1.5") - internet
    internet - Edge(minlen="1.5") - isp_2 - Edge(minlen="1.5") - router_2

with Diagram("", filename="simple", show=False, outformat="jpg", graph_attr=graph_attr):
    local_1 = [
        Client("192.168.1.10"),
        Client("192.168.1.11"),
        Mobile("192.168.1.12"),
    ]

    router_1 = Router("Routeur")
    local_1 - router_1

with Diagram(
    "", filename="private", show=False, outformat="jpg", graph_attr=graph_attr
):
    with Cluster("Réseau local"):
        local_1 = [
            Client("192.168.1.10"),
            Client("192.168.1.11"),
            Mobile("192.168.1.12"),
        ]

        router_1 = Router("Routeur")
        local_1 - router_1

    isp_1 = Switch("ISP")

    with Cluster("Réseau public", direction="TB", graph_attr={"style": "invis"}):
        internet = Domain("")
        server = Rack("raspberrypi.com\n172.67.154.53")

        internet - Edge(constraint="false") - server

    router_1 - Edge(minlen="1.5") - isp_1 - Edge(minlen="1.5") - internet

with Diagram("", filename="vpn", show=False, outformat="jpg", graph_attr=graph_attr):
    with Cluster("Réseau local A"):
        local_1 = [
            Client("192.168.1.10"),
            Client("192.168.1.11"),
            Mobile("192.168.1.12"),
        ]

        router_1 = Router("Routeur")
        local_1 - router_1

    isp_1 = Switch("ISP")

    with Cluster("Réseau public", direction="TB", graph_attr={"style": "invis"}):
        dns = Rack("DNS\n1.1.1.1")
        internet = Domain("")
        server = Rack("raspberrypi.com\n172.67.154.53")

        dns - Edge(constraint="false") - internet
        internet - Edge(constraint="false") - server

    isp_2 = Switch("ISP")

    with Cluster("Réseau local B"):
        local_2 = [
            VPN("192.168.1.11"),
            Mobile("192.168.1.10"),
            Client("192.168.1.9"),
        ]

        router_2 = Router("Routeur")
        router_2 - local_2

    router_1 - Edge(minlen="1.5") - isp_1 - Edge(minlen="1.5") - internet
    internet - Edge(minlen="1.5") - isp_2 - Edge(minlen="1.5") - router_2
