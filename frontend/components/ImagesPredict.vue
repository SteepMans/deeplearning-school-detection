<template>
    <div class="predict">
        <div v-for="(item, index) in images" :key="index" class="predict__images">
            <img :src="item.url">
            <div v-for="predict in item.predict" :key="index" class="predict__text">
                132
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["images"],

    data () {
        return {
        }
    },

    methods: {
      
    },

    created() {
        for (var item of this.images) {
            const defualtImageWidth = 0;
            const defualtImageHeight = 0;
            
            console.log(document.getElementsByClassName('predict__images'))
        }
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
    }

    &__text {
        position: absolute;
        top: 0;
        left: 30px;
    }
}
</style>