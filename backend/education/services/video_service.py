import logging
import os
from urllib.parse import quote
from django.http import HttpResponse, FileResponse
from django.core.files.storage import default_storage
from education.models import Video

logger = logging.getLogger(__name__)


class VideoService:
    """
    Service class for video-related business logic
    """
    
    @staticmethod
    def reorder_videos(queryset, new_order):
        """
        Reorder videos based on the provided order list
        
        Args:
            queryset: QuerySet of videos to reorder
            new_order: List of video IDs in the new order
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            videos_to_update = []
            
            for index, video_id in enumerate(new_order):
                try:
                    video = queryset.get(id=video_id)
                    video.order = index
                    videos_to_update.append(video)
                except Video.DoesNotExist:
                    continue

            if videos_to_update:
                Video.objects.bulk_update(videos_to_update, ['order'])
            
            return True, 'ترتیب ویدیوها با موفقیت تغییر کرد'
        except Exception as e:
            logger.error(f"Error reordering videos: {e}", exc_info=True)
            return False, 'خطا در تغییر ترتیب ویدیوها'
    
    @staticmethod
    def prepare_video_download(video):
        """
        Prepare video file for download - works for both local and cloud storage
        
        Args:
            video: Video instance
            
        Returns:
            tuple: (success: bool, response_or_error: HttpResponse or str)
        """
        try:
            if not video.video_file or not default_storage.exists(video.video_file.name):
                return False, 'فایل ویدیو یافت نشد'

            video.increment_download_count()
            file_name = os.path.basename(video.video_file.name)
            file_path = getattr(video.video_file, 'path', None)

            try:
                if file_path and os.path.exists(file_path):
                    # local file
                    response = FileResponse(
                        open(file_path, 'rb'),
                        content_type='application/octet-stream'
                    )
                else:
                    # cloud file
                    with default_storage.open(video.video_file.name, 'rb') as f:
                        response = HttpResponse(f.read(), content_type='application/octet-stream')

                response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
                return True, response

            except Exception as e:
                logger.error(f"Error serving file: {e}", exc_info=True)
                return False, 'خطا در دانلود فایل'
                
        except Exception as e:
            logger.error(f"Error in prepare_video_download: {e}", exc_info=True)
            return False, 'خطای ناشناخته در دانلود فایل'
