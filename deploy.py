import argparse
import os

APPS = ['img-panda', 'smart-panda', 'all']
PLAYBOOK_NAME = 'base.yml'


def configure_arg_parser(parser):
    parser.add_argument("-a", "--apps",
                        choices=APPS, help="App name",
                        metavar="APP_NAME",
                        required=True)
    parser.add_argument('--inventory', '-i',
                        required=True,
                        metavar="INVENTORY_PATH",
                        help='The path of the Ansible Inventory will be used')
    parser.add_argument('--key', '-k',
                        required=False,
                        metavar="PRIVATE_KEY_PATH",
                        help='SSH key to be used')
    parser.add_argument('--user', '-u',
                        required=False,
                        metavar="USERNAME",
                        help='Which user will to use in order to SSH')
    return parser


def get_shell_cmd(inventory, app, private_key=None, user=None):
    if app == 'all':
        app = [a for a in APPS if a != 'all']

    cmd = 'ansible-playbook -i {inventory} --tags "{apps},common" ' \
          '{private_key} {user} {playbook}'\
          .format(inventory=inventory, apps=','.join(app),
                  private_key=('--private-key ' + private_key) if private_key
                                                               else '',
                  user='-u' + user if user else '',
                  playbook=PLAYBOOK_NAME)
    return cmd


def main():
    parser = argparse.ArgumentParser()
    configure_arg_parser(parser)
    args = parser.parse_args()
    shell_cmd = get_shell_cmd(inventory=args.inventory,
                              app=args.app,
                              private_key=args.key,
                              user=args.user)
    os.system(shell_cmd)

if __name__ == '__main__':
    main()