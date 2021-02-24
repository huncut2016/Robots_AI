class Map {
    constructor (population) {
        this.population = population;
        this.caracters = [];
        for(let i = 0; i < population; i++){
            let caracter;
            caracter = new Caracter({
                x: Math.floor(Math.random() * width),
                y: Math.floor(Math.random() * height),
                demage: 200,
                velocity: 1, 
                bulletVelocity: 5,
                HP: 200,
                capacity: 10,
                reloadTime: 3000,
                direction: Math.random() * PI * 2,
                ID: i
                
            });


            this.caracters.push(caracter);
        }
        this.bullets = [];
        this.rankCounter = 0;

    }

    update () {
        this.caracters = this.caracters.map(caracter => {
            if (!caracter.visible) return caracter;

            this.bullets = this.bullets.filter(bullet => {
                if(bullet.ID === caracter.ID) return true;

                if(bullet.pos.dist(caracter.pos)< 15){
                    caracter.HP -= bullet.demage;
                    alert("meghalt");    
                    return false;
                }
                return true;

            })
            caracter.update();
            let shot = caracter.shot();


            if( shot != undefined) {
                this.bullets.push(shot);
            }


            if(
                caracter.pos.x < 0 || 
                caracter.pos.x > width ||
                caracter.pos.y < 0 ||
                caracter.pos.y > height ||
                caracter.HP <= 0
                
            ){
                this.rankCounter ++;
                caracter.visible = false;
                console.log(true)
                caracter.rank = this.rankCounter;
                if (this.rankCounter === this.population) {
                    alert("Megdöglött az összes");
                }
            }
            return caracter;
        });

       this.bullets = this.bullets.filter(bullet => {
            bullet.update();
            return !(
                    bullet.pos.x < 0 || 
                    bullet.pos.x > width ||
                    bullet.pos.y < 0 ||
                    bullet.pos.y > height
                )
        })
    }

    show () {
        this.caracters.forEach(caracter => {
            if(!caracter.visible) return;
            caracter.show();
        });

        this.bullets.forEach(bullet => {
            bullet.show();
        });
    }
}