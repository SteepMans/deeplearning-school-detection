<template>
    <div class="predict">
        <div v-for="(item, index) in scaleImages" :key="index" class="predict__images">
            <img :src="item.url" class="predict__image" ref="predictImage">
            <div v-for="(predict, predictIndex) in item.predict" :key="predictIndex" class="predict__text" :style="{'border': `3px solid ${getRandomColor()}`, 'top' : `${predict.ymin}px`, 'left': `${predict.xmin}px`, 'height': `${predict.height}px`, 'width': `${predict.width}px`}">
                {{ predict.name }} <br> {{ predict.confidence.toFixed(3) }}
            </div>
        </div>
    </div>
</template>

<script>
import { cloneDeep } from 'lodash-es'

export default {
    props: ["images"],

    data () {
        return {
            scaleImages: null
        }
    },

    methods: {
        confidenceRound(value) {
            return Math.round10(value, -1);
        },

        getRandomColor() {
            var letters = '0123456789ABCDEF';
            var color = '#';

            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            
            return color;
        },

        rescaleImage() {
            const clientImageWidth = 581;
            const clientImageHeight = 363;  

            for (var item of this.scaleImages) {
                const defualtImageWidth = item.naturalSize.width;
                const defualtImageHeight = item.naturalSize.height;
    
                var scaleWidth = clientImageWidth * 100.0 / defualtImageWidth / 100;
                var scaleHeight = clientImageHeight * 100.0 / defualtImageHeight / 100;
    
                for (var predict of item.predict) {
                    predict.ymin = predict.ymin * scaleHeight;
                    predict.ymax = predict.ymax * scaleHeight;

                    predict.xmin = predict.xmin * scaleWidth;
                    predict.xmax = predict.xmax * scaleWidth;

                    predict.width = predict.xmax - predict.xmin;
                    predict.height = predict.ymax - predict.ymin;
                }

                console.log(predict)
            }
        }
    },

    mounted() {
        setTimeout(() => {
            this.scaleImages = cloneDeep(this.images);
            this.rescaleImage();
        }, 1);
    }
}
</script>

<style lang="scss">
.predict {
    &__images {
        position: relative;
    }

    img {
        width: 50%;
        height: 50%;
        background-size: cover;
        overflow: auto;
    }

    &__text {
        display: grid;
        align-items: center;
        justify-content: center;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 300%;
        border-radius: 10px;
        position: absolute;
        text-align: center;
        text-shadow: 1px 1px 1px #000;
        line-height: 40px;
    }
}
</style>