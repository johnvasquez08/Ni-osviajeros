using UnityEngine;
using UnityEngine.SceneManagement; // Necesario para manejar escenas

public class ChangeSceneButton : MonoBehaviour
{
    public string sceneName; // Nombre de la escena a cargar

    public void ChangeScene()
    {
        if (!string.IsNullOrEmpty(sceneName))
        {
            SceneManager.LoadScene(sceneName); // Cambia a la escena especificada
        }
        else
        {
            Debug.LogWarning("El nombre de la escena no está configurado.");
        }
    }
}