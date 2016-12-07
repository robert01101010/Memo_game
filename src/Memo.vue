<template>
  <div class="memo">
    <div class="memo-cards-container">
      <div class="memo-card" v-for="cardPath in cards" @click="showBottom(cardPath, $event)">
        <button class="memo-card__front" ref="front"></button>
        <button class="memo-card__back" v-bind:style="{ backgroundImage: 'url(' + cardPath + ')'}" disabled></button>
      </div>
    </div>
    <div class="memo-aside">
      <div class="memo-aside__score">
        Points: {{value}}
      </div>
      <div class="memo-aside__move">
        Turns: {{move}}
      </div>
      <button class="memo-aside__button memo-aside__button--level" @click="reset('easy')">Easy</button>
      <button class="memo-aside__button memo-aside__button--level" @click="reset('medium')">Medium</button>
      <div class="memo-aside-lastScores">
        Scores Table
        <ul class="memo-aside-lastScores" v-for="score in lastScores"> 
          <li class="memo-aside-lastScores__singleScore">turns {{score.turn}} points {{score.value}}</li>
        </ul>
      </div>
    </div>
    <div class="memo-score" v-bind:class="isWin">
      <div class="memo-score__win">
        Won in {{move}} turns.
      </div>
      <button class="memo-score__again" @click="reset">
        Click to play again
      </button>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'memo',
    data() {
      return {
        maxAction: 2,
        currentAction: 0,
        cardsElems: [],
        value: 0,
        move: 0,
        cards: [],
        isWin: '',
        isTransform: '',
        transformClass: 'memo-card__front--transform',
        lastScores: [],
      };
    },
    created() {
      this.initLevel('easy');
    },
    methods: {
      initLevel(gameLevel) {
        const easyPictures = [
          'https://s6.postimg.org/bskqajpst/image.png',
          'https://s6.postimg.org/65odd2na5/image.png',
          'https://s6.postimg.org/5hfiu4okd/image.png',
          'https://s6.postimg.org/ob1br4msd/image.png',
          'https://s6.postimg.org/sy7dswa59/image.png',
          'https://s6.postimg.org/bm717ggnx/image.png'];

        const mediumPictures = (() => {
          const restPictures = [
            'https://s6.postimg.org/fjuawv3h9/image.png',
            'https://s6.postimg.org/gnef8to4d/image.jpg'];
          return restPictures.concat(easyPictures);
        })();

        let pictures = '';
        switch (gameLevel) {
          case 'easy':
            pictures = easyPictures;
            break;
          case 'medium':
            pictures = mediumPictures;
            break;
          default:
            pictures = easyPictures;
        }
        this.initCards(pictures);
      },
      initCards(cards) {
        const paths = [];
        for (let x = 0; x < this.maxAction; x += 1) {
          for (let y = 0; y < cards.length; y += 1) {
            paths.push(cards[y]);
          }
        }
        this.cards = this.mixArray(paths);
        return;
      },
      mixArray(array) {
        const arr = array;
        for (let i = 0; i < arr.length; i += 1) {
          const random = Math.floor(Math.random() * arr.length);
          const temp = arr[i];
          arr[i] = arr[random];
          arr[random] = temp;
        }
        return arr;
      },
      showBottom(cardPath, evt) {
        const targetCard = evt.target;
        targetCard.classList.add(this.transformClass);

        this.cardsElems.push({
          card: targetCard,
          path: cardPath,
        });
        this.currentAction += 1;
        this.checkAmountOfAction();
      },
      checkAmountOfAction() {
        if (this.currentAction >= this.maxAction) {
          this.move += 1;
          if (this.gainPoint()) {
            this.currentAction = 0;
            this.cardsElems = [];
            return;
          }
          this.hideCards(200);
        }
      },
      hideCards(delay) {
        const timeOut = delay || 200;
        setTimeout(() => {
          for (let i = 0; i < this.cardsElems.length; i += 1) {
            this.cardsElems[i].card.classList.remove(this.transformClass);
          }
          this.currentAction = 0;
          this.cardsElems = [];
        }, timeOut);
      },
      gainPoint() {
        let valueTocheck = '';
        for (let i = 1; i < this.cardsElems.length; i += 1) {
          valueTocheck = this.cardsElems[i - 1].path;
          if (this.cardsElems[i].path === valueTocheck) {
            this.value += 1;
            if (this.value === this.cards.length / 2) {
              this.updateScoreTable();
              this.isWin = 'memo-score--active';
            }
            return true;
          }
        }
        return false;
      },
      updateScoreTable() {
        if (this.lastScores.length >= 4) {
          this.lastScores.shift();
        }
        this.lastScores.push({
          turn: this.move,
          value: this.value,
        });
      },
      reset(gameLevel) {
        this.currentAction = 0;
        this.cardsElems = [];
        this.value = 0;
        this.move = 0;
        this.cards = [];
        this.isWin = '';
        for (const card of this.$refs.front) {
          card.classList.remove(this.transformClass);
        }
        this.initLevel(gameLevel);
      },
    },
  };
</script>
<style lang="scss">
  @import "./style/reset.scss";
  @import "./style/variables.scss";
  @import "./style/mixin.scss";
  
  .memo {
    display: flex;
  }
  .memo-cards-container {
    margin-top: $margin-top;
    background: $cards-container-background;
    width: 75%;
    margin-left: 5%; 
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    perspective: 1000px;
    border-radius: 10px 0 0 10px;
  }
  .memo-card {
    width: calc(16.6666% - 40px);
    @include bp-large {
      width: calc(25% - 40px);
      height: 140px;
    }
    @include bp-medium {
      width: calc(33.3333% - 40px);
      height: 100px;
    }
    @include bp-small {
      width: calc(33.3333% - 40px);
      height: 100px;
    }
    @include bp-very-small {
      width: calc(50% - 40px);
      height: 100px;
    }
    height: 160px;
    margin: 10px;
    transition: 0.6s;
    transform-style: preserve-3d;
    position: relative;
    &__front, &__back {
      border-radius: 12px;
      backface-visibility: hidden;
      background-size: 100% 100%;    
      background-repeat: no-repeat;      
      position: absolute;
      top: 0;
      left: 0;
      height:100%;
      width:100%;
    } 
    &__front {
      background-image: url('https://s6.postimg.org/f1ltv5qox/card.jpg');
      z-index: 2;
      &--transform {
        transform: rotateY(180deg);
      }
      &:hover {
        cursor: pointer;
      }
    }
  }
  .memo-aside {
    background: $aside-background;
    margin-top: $margin-top;
    padding: 10px;
    color: white;
    text-align: center;
    margin-rigth: 5%;
    width: 15%;
    border-radius: 0 10px 10px 0;
    &__score, &__move {
      @include font-size(22px)
      background: black;
      margin-bottom: 2px;
      @include bp-medium {
        @include font-size(14px)
      }
    }
    &__button {
      @include font-size(22px)
      background: $aside-background__button;
      width: 100%;
      height: 40px;
      border: 1px solid black;
      margin-bottom: 2px;
      border-radius: 5px;
      font-weight: 500;
      @include bp-medium {
        @include font-size(14px)
      }
      &:hover {
        cursor: pointer;
        background: $aside-background__button--hover;
      }
      &--level {
        display: block;
      }
    }
  }
  .memo-score {
    position: absolute;
    background: black;
    opacity: 0.8;
    width: 100%;
    height: 100%;
    border-radius: 5px;
    border: 1px solid black;
    visibility: hidden;
    animation: 1s fadeIn;
    animation-fill-mode: forwards; 
    &--active {
      visibility: visible;
    }
    &__win {
      background: white;
      margin-top: 15%;
      text-align: center;
      height: 80px;
      line-height: 80px;
      font-size: 2em;
      font-weight: bold;
    }
    &__again {
      margin-top: 30px;
      text-align: center;
      height: 80px;
      line-height: 80px;
      font-size: 2em;
      font-weight: bold;
      width: 100%;
      &:hover {
        cursor: pointer;
      }
    }
  }
  .memo-aside-lastScores {
    color: white;
    font-size: 18px;
    border: 1px solid white;
    margin: 5px;
    padding: 2px;
  }
</style>
