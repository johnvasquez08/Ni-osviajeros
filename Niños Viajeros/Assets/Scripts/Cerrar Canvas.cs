using UnityEngine;

public class CloseCanvasButton : MonoBehaviour
{
    public GameObject canvasToClose; // Arrastra aquí el Canvas desde el Inspector

    public void CloseCanvas()
    {
        if (canvasToClose != null)
        {
            canvasToClose.SetActive(false); // Desactiva el Canvas
        }
    }
}