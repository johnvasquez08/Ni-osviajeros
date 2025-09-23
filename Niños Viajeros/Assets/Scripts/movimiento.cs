using UnityEngine; 
using UnityEngine.InputSystem; 

public class PlayerMovement : MonoBehaviour 
{ 
    public float speed = 5f; 
    private Rigidbody2D rb; 
    private Vector2 moveInput; 
    private SpriteRenderer spriteRenderer; 

    void Start() 
    { 
        rb = GetComponent<Rigidbody2D>(); 
        spriteRenderer = GetComponent<SpriteRenderer>(); // 👈 Agarramos el SpriteRenderer 
    } 

    void Update() 
    { 
        rb.linearVelocity = moveInput * speed; //Hacer flip según la dirección horizontal 
        if (moveInput.x > 0.01f) // va a la derecha 
        { 
            spriteRenderer.flipX = true; 
        } 
        else if (moveInput.x < -0.01f) // va a la izquierda 
        { 
            spriteRenderer.flipX = false; 
        } 
    } 

    void OnMove(InputValue value) 
    { 
        moveInput = value.Get<Vector2>(); 
    } 
}