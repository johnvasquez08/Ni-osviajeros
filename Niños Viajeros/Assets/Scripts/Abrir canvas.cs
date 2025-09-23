using UnityEngine;

public class OpenCanvasButton : MonoBehaviour
{
    public GameObject canvasToOpen; // Arrastra aquí el Canvas desde el Inspector

    public void OpenCanvas()
    {
        if (canvasToOpen != null)
        {
            canvasToOpen.SetActive(true); // Activa el Canvas
        }
    }
}