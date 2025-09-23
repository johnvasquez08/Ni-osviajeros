using UnityEngine;

public class PopupTrigger : MonoBehaviour
{
    public PopupManager popupManager;

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player")) // Asegurarse de que el jugador tenga el tag "Player"
        {
            popupManager.ShowPopup();
        }
    }
}