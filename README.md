## Explaining how things work

- Initially I was not so bothered about even making a readme in the first place but as time went on and things got bigger, I had to.
- At this point what I have craeted is somewhat a physics engine or sandbox at this point tbh. But yes with limited capabilities.
- Okay so here are the things I want to explain, this is also a note to my future self in God knows how many years, cause I tend to leave things as is and abandon prjects quite often wihtout implementing everything i initially thought of

## THE LOGIC 

### I will begin with the easiet part first.

#### THE PLAYER

- You will notice I have functions for moving left, right and jumping around.
- I feel like these functions are quite self explanatory with the comments I(actually 'WE') left (funfact: I was forced by a person to leave comments, credit where it's due, he also helped me with organising stuff, else the entire codebase was a mess)

#### THE MOVABLES

###### COLLISIONS!!!!!!!!!!!

- I could write an entire essay about it, But here's the summary


- Each object wether movable or immovable scans it's surroundings and sets the paramaeters like roof, floor, etc of any entity in it's vicinity, so no its not the player scanning its surroundings, its the player being fed to the functions of movables and immovables that then take the player's parameters, check if there is a collision or if its floor or roof values needs to be updated and then updates those parameters of the player_obj accordingly. Idk why i went with this approach but it works so ill move forward with it.



