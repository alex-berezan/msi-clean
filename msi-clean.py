import os
from xml.dom.minidom import parse
from subprocess import call

def node_to_product_version(product_version_node):
    return ( product_version_node.attributeValue('name'), product_version_node.attributeValue('version'), product_version_node.attributeValue('product-id'))

def nodes_to_product_versions(product_node):
    product_versions = []
    for product_version_node in product_node:
        product_versions.append(node_to_product_version(product_version_node))
    return product_versions

def get_product_versions(dom, product_family_name):
    for node in dom.getElementsByTagName('product-family'):
        if node.attributeValue('name') == product_family_name:
            return nodes_to_product_versions(node)

    raise("Unable to find product-family '{0}'".format(product_family_name))

def exec_msi_uninstall(product_version):
    (name, version, product_id) = product_version

    command = "msiexec /x {0} /q".format(product_id)
    message = "Uninstalling '{0} v{1}' via command {2}".format(name, version, command)
    
    call (['msiexec', '/x', product_id, '/q'])

if __name__ == "__main__":
    product_family_name = "sample-product-1"# sys.argv[1]
    file_path = 'products.xml'

    print "Uninstalling product-family '{0}' ...".format(product_family_name)
    print "Opening file '{0}' ...".format(file_path)
    dom1 = parse(file_path)

    print "Looking for product-family-node with name = '{0}' ...".format(product_family_name)
    product_versions = get_product_versions(dom1, product_family_name)

    print "Node found."
    for product_version in product_versions:
        exec_msi_uninstall(product_version)

    print "Uninstallation completed."