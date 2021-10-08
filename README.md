# T-Project
A community tool for people on their energy transition journey


## Wireframe

<span><img src="https://github.com/Op-Design/T-Project/blob/main/Wireframes/Draft%201%20Images/Login.png" alt="wireframe image png" style="width:230;height:244px;"></span>
<span><img src="https://github.com/Op-Design/T-Project/blob/main/Wireframes/Draft%201%20Images/Sign%20Up.png" alt="wireframe image png" style="width:230;height:244px;"></span>
<span><img src="https://github.com/Op-Design/T-Project/blob/main/Wireframes/Draft%201%20Images/Energy%20Usage.png" alt="wireframe image png" style="width:230;height:244px;"></span>
<span><img src="https://github.com/Op-Design/T-Project/blob/main/Live%20Images/T-Project.jfif" alt="live dashboard jfif" style="width:230;height:244px;"></span>

## Example Code

```
def registration(request):
    if request.method == "GET":
        return render (request, 'registration.html')
    elif request.method == "POST":
        # Validates input data meets standards in models
        errors = User.objects.registration_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/registration')
        # Sends data and creates objects if everything is verified
        else:
            password = request.POST['password']
            . . . hidden . . .
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
            # Saves data in sessions for future use.
            request.session['user_id'] = new_user.id
            request.session['first_name']=new_user.first_name
            return redirect('/homes')
    else:
        return redirect ('/')
```