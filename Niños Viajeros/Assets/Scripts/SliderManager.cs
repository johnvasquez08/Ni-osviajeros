using UnityEngine;

public class SlideManager : MonoBehaviour
{
    public GameObject[] slides; // Array de diapositivas
    private int currentSlideIndex = 0;

    void Start()
    {
        HideAllSlides(); // Asegúrate de que todas las diapositivas estén ocultas al inicio
    }

    public void ShowSlide(int index)
    {
        HideAllSlides();
        slides[index].SetActive(true);
        currentSlideIndex = index;
    }

    public void NextSlide()
    {
        currentSlideIndex = (currentSlideIndex + 1) % slides.Length; // Movimiento cíclico hacia adelante
        ShowSlide(currentSlideIndex);
    }

    public void PreviousSlide()
    {
        currentSlideIndex = (currentSlideIndex - 1 + slides.Length) % slides.Length; // Movimiento cíclico hacia atrás
        ShowSlide(currentSlideIndex);
    }

    private void HideAllSlides()
    {
        foreach (GameObject slide in slides)
        {
            slide.SetActive(false);
        }
    }

    public void OpenFirstSlide()
    {
        ShowSlide(0); // Abre la primera diapositiva
    }

    public void CloseSlides()
    {
        HideAllSlides(); // Oculta todas las diapositivas
    }
}