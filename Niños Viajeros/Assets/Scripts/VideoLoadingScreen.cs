using UnityEngine;
using UnityEngine.Video;

public class VideoLoadingScreen : MonoBehaviour
{
    public Canvas loadingCanvas; // Canvas que contiene el video

    private VideoPlayer videoPlayer;

    private void Start()
    {
        // Obtén el componente VideoPlayer
        videoPlayer = GetComponent<VideoPlayer>();

        // Suscríbete al evento que se dispara cuando el video termina
        videoPlayer.loopPointReached += OnVideoEnd;
    }

    private void OnVideoEnd(VideoPlayer vp)
    {
        // Oculta el Canvas cuando el video finaliza
        loadingCanvas.gameObject.SetActive(false);
    }
}