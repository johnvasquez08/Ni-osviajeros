using UnityEngine;

public class PopupManager : MonoBehaviour
{
    public GameObject popupUI; // Asignar el popup desde el editor
    public Collider2D triggerCollider; // Asignar el Collider desde el editor
    private PlayerMovement playerMovement;
    private Rigidbody2D playerRigidbody;

    void Start()
    {
        popupUI.SetActive(false); // Asegurarse de que el popup esté desactivado al inicio
        playerMovement = FindFirstObjectByType<PlayerMovement>();
        playerRigidbody = FindFirstObjectByType<Rigidbody2D>();
    }

    public void ShowPopup()
    {
        popupUI.SetActive(true);

        // Deshabilitar el movimiento del jugador
        if (playerMovement != null)
        {
            playerMovement.enabled = false;
        }

        // Detener completamente al jugador
        if (playerRigidbody != null)
        {
            playerRigidbody.linearVelocity = Vector2.zero; // Detener la velocidad
            playerRigidbody.angularVelocity = 0f; // Detener la rotación
            playerRigidbody.bodyType = RigidbodyType2D.Kinematic; // Cambiar a Kinematic
        }
    }

    public void ClosePopup()
    {
        popupUI.SetActive(false);

        // Habilitar el movimiento del jugador
        if (playerMovement != null)
        {
            playerMovement.enabled = true;
        }

        // Restaurar el Rigidbody2D a su estado original
        if (playerRigidbody != null)
        {
            playerRigidbody.bodyType = RigidbodyType2D.Dynamic; // Cambiar a Dynamic
        }

        // Deshabilitar temporalmente el Collider
        if (triggerCollider != null)
        {
            triggerCollider.enabled = false;
            Invoke(nameof(EnableCollider), 2f); // Rehabilitar el Collider después de 2 segundos
        }
    }

    private void EnableCollider()
    {
        if (triggerCollider != null)
        {
            triggerCollider.enabled = true;
        }
    }
}