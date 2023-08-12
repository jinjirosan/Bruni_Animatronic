# Bruni Animatronic

Last time I was at Disneyland Paris and saw various Disney and Pixar characters used as shoulder plushies. They were so cute and popular that they were sold out by the time I got to the gift shop. Inspired by Disney's Imagineers and animatronic artists, I decided to buy one online and make it totally unique for our next trip to Disney. 


I wanted to create an animatronic shoulder plushie of Bruni, the fire-breathing salamander from Frozen. With the help of a Pimoroni Pico LiPo, Tower Pro SG92R servo, Flora Neopixel, and kitelight bright EL-Wire, I was able to bring Bruni to life. I used MicroPython v1.19.1 to code the movements and light effects, and now Bruni is ready to accompany us on our next Disney adventure.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1683.jpeg)
###### --> image: Bruni

## hardware platform (v1.1-2023/04 for codebase v4-x.x)
- Pimoroni Pico Lipo 4Mb board
- Galleon LiPo 3.7v - 400 mAh (in hardcase shell)
- TowerPro SG92R servo to control the tailwagging motion
- Adafruit Flora RGB Neopixel V2
- two microswitches (clickety-click textile style), one in each front paw
- 18mm sewable Neo-Dymium magnet (can hold 1.9kg) for Bruni
- 18mm sewable Neo-Dymium magnet + 25mm Neo-Dymium magnet (can hold 3.1kg) for shoulder patch base.

## Bruni in action
- The microswitch in his front-right-paw activates the flame. The flame simulates a 'natural' fire-breathing dragon in purple-pink flames in various brightness.
- The microswitch in his front-left-paw activates his tail-wagging-function. The tailwag is simulating 'natural' behavior in 4 stages (2 to the left and 2 to the right). The angle or range of each wag is randomized.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1684_MOV-demo.gif)

## Build process

A not-so-short impression of the build process going from 'just' the pluche animal to the animatronic version.


First off, an overview of the components used. You see the EL-Wire included here however I have not yet integrated this on Bruni's back. I was thinking to outline his purple markings but found it challenging to integrate. So giving it some more thought.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1705-components.jpeg)
###### --> image: components

Little bit of a nervous moment cutting Bruni open to be able to insert all the components. I've sewn in a piece of velcro so I can still charge the LiPo and work on Bruni's components.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1643-velcro.jpeg)
###### --> image: Create an opening to get the animatronic components in and sew in velcro

I've sewn in a strong magnet inside Bruni. The 'plate' that Bruni sits on is an old plastic card with two supermagnets glued to it and encased in soft fabric.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1644-magnet.jpeg)
###### --> image: Add a strong magnet to keep Bruni in-place on my shoulder

I've made the original version of the tail wagging motion but found that the round 3D printed sections were rubbing the top/bottom of Bruni's skin deforming the tail's shape. So I drew new ones. On the right the original tail version, on the left the 2.0 version. The sleeker 3D printed sections fit Bruni better.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1675-tail-versions.jpeg)
###### --> image: 1.0 right, 2.0 left

First time testing the tailwag and holding Bruni over the component to see how wide the range would be.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1571_MOV-tailwag-test.gif)
###### --> image: tailwag testing

I'm using a Snapmaker A250 for all my builds as this platform can 3D print, CNC, laser engrave and cut. Here you see the CNC head in action cutting out the flame from a piece of transparent plexiglass.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1604_MOV-cutting-flame.gif)
###### --> image: CNC-ing the flame

The custom designed and CNC'd flame from transparent plexiglass, the custom made 3D printed mount/bracket and the Flora pixel make up the components for the flame.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1635-flame-components.jpeg)
###### --> image: flame components breakdown

Testing the flame function, it is bright in full darkness, maybe I'll add a lightsensor to compensate.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1634_MOV-flame-test.gif)
###### --> image: Flame test

Attached the flame to Bruni. No glue needed, the bracket holds the flame tight. After two Disney trips, the flame is still securely fastened.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1679-flame-attached.jpeg)
###### --> image: flame attached

The animatronic tail goes in, it is a very tight fit. The bottom plate is not yet attached to the servo so I have a bit more wiggle room. Next is adding the stuffing back to fill up the tail.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1677-inserting-tail.jpeg)
###### --> image: Inserting tail components

Finally, the final piece is adding the heart to Bruni.

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1681-inserting-heart.jpeg)
###### --> image: Inserting Bruni logicboard

This is how Bruni can be easily re-charged

![Bruni](https://github.com/jinjirosan/Bruni_Animatronic/blob/main/images/IMG_1725-charging-bruni.jpeg)
###### --> image: Charging Bruni
