from django.core.management.base import BaseCommand
from pezAutomatization import upload_video_ws, delete_video_ws
from pezAutomatization import send_mail, delete_local_videos


class Command(BaseCommand):
    help = 'Tasks for automatizations peztech (3 task necessaries)'

    def add_arguments(self, parser):
        print("Entrando en arguments")
        # parser.add_argument('poll_ids', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument('--upload', action='store_true', help='Upload Stream')
        parser.add_argument('--delete-local', action='store_true', help='Delete olds video recording')
        parser.add_argument('--delete-ms', action='store_true', help='Delete olds video in MS')
        parser.add_argument('--send-email', action='store_true', help='Test email')

    def handle(self, *args, **options):
        print("Entrando en handle")

        if options['upload']:
            print("En upload")
            upload_video_ws.start_ws()
        elif options['delete_local']:
            print("En delete local")
            delete_local_videos.process_delete_local_videos()
        elif options['send_email']:
            print("send_email")
            send_mail.send_notification("nombre de prueba")
        elif options['delete_ms']:
            print("En delete MS")
            delete_video_ws.process_ws()
        else:
            print("Sin argumentos, cerrando...")
