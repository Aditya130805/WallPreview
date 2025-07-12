<template>
    <section class="landing_container">
        <header>
            <a href="#" class="logo"><div></div></a>
            <nav>
                <ul>
                    <li class="nav_items"><a href="#">Home</a></li>
                    <li class="nav_items"><a href="#all_wallpapers">Wallpapers</a></li>
                    <li><button class="sign-in" style="display: none;">Sign in</button></li>
                </ul>
            </nav>
        </header>
        <main class="home_container">
            <div class="preview-box"></div>
            <div class="description">
                <h1>Ditch the Decor Dilemmas: Try <span>WallPreviews</span></h1>
                <p>Upload a picture of your wall and crop it to fit your dimensions, without worrying about any items in front of it. Browse by style, and see wallpapers come to life in your space.</p>
                <router-link to="/app" class="try-now">Try it now! (Free)</router-link>
            </div>
        </main>
    </section>
    <section class="why_us">
        <h2>Why <span class="logo">WallPreviews</span>?</h2>
        <div class="cards">
            <div class="card">
                <img class="icon" style="width: 50%;" :src="require('../assets/Images/Time.png')" alt="Time Icon">
                <div class="card_text">
                    <h3>Save Time & Money</h3>
                    <p>Avoid costly mistakes by visualizing your chosen wallpaper in your space before making a purchase.</p>
                </div>
            </div>
            <div class="card">
                <img class="icon" :src="require('../assets/Images/Confidence.jpg')" alt="Confidence Icon">
                <div class="card_text">
                    <h3>Confidence in Choice</h3>
                    <p>Make informed decisions with realistic previews, ensuring satisfaction in your selection and confidence in your decision as you finalize your custom home decor.</p>
                </div>
            </div>
            <div class="card">
                <img class="icon" :src="require('../assets/Images/Creative.jpg')" alt="Creativity Icon">
                <div class="card_text">
                    <h3>Enhanced Creativity</h3>
                    <p>Experiment with different designs and colors to find the perfect look for your home.</p>
                </div>
            </div>
        </div>
    </section>
    <section class="wallpapers_container" id="all_wallpapers">
        <h2>Explore countless wallpapers!</h2>
        <div class="wallpapers_grid">
            <img class="wallpaper" v-for="wallpaper in wallpapers" :key="wallpaper" :src="require(`@/assets/Wallpapers/${wallpaper}`)">
        </div>
    </section>
    <section class="contact">
        <h2>Get in touch!</h2>
        <form class="contact_form" autocomplete="off" action="https://formsubmit.co/aditya130805@gmail.com" method="POST">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required>
            <label for="message">Query / Concern / Feedback (Anything is welcome!)</label>
            <textarea id="message" name="message" rows="6" required></textarea>
            <button type="submit">Submit</button>
        </form>
    </section>
    <section class="footer">
        <p>Copyright © 2024 WallPreviews. All rights reserved.</p>
    </section>
</template>

<script>
import constants from '@/assets/constants.json';

export default {
    name: 'HomePage',
    data() {
        return {
            wallpapers: constants.ALL_WALLPAPERS
        };
    }
}
</script>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        scroll-behavior: smooth;
    }
    html {
        scroll-behavior: smooth;
    }

    :root {
        --base-color: #d0ddd0;
        --base-lighter-color: #e0eee0;
        --highlight-color: #12664f;
        --highlight-darker-color: #045847;
        --placeholder-color: gray;
        --black-color: black;
        --white-color: white;
        --off-white-color: rgb(220, 220, 220);
        --footer-color: rgb(40, 40, 40);
    }

    /************ LANDING HOME PAGE SECTION ************/

    .landing_container {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    header {
        height: 110px; /* TODO: Might change */
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 50px; /* TODO: Might change */
        margin: 0;
        background-color: var(--base-color);
    }
    
    .logo {
        font-family: 'Comic Sans MS', 'Comic Neue', 'EMcomic', 'Geneva', 'Verdana', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--black-color);
        text-decoration: none;
    }
    .logo div {
        background: url('../assets/logo.png');
        width: 162px;
        height: 80px;
        background-position: center;
        background-size: cover;
        filter: hue-rotate(100deg) brightness(0.5) contrast(1.2);
    }
    
    nav ul {
        list-style: none;
        display: flex;
        gap: 40px;  /* TODO: Might change */
        padding: 0;
    }
    
    nav ul li {
        display: flex;
        align-items: center;
        position: relative;
    }
    nav ul li a {
        text-decoration: none;
        color: var(--black-color); /* TODO: Might change */
        font-size: 18px;  /* TODO: Might change */
        position: relative;
        padding: 5px 0;  /* TODO: Might change */
    }

    .nav_items::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        left: 0;
        bottom: 0;
        background-color: var(--highlight-color); /* TODO: Might change */
        transition: width 0.3s ease;
    }

    .nav_items:hover::after {
        width: 100%;
    }
    
    .sign-in {
        background-color: var(--highlight-color);
        color: var(--white-color); /* TODO: Might change */
        font-size: 16px;
        border: none;
        padding: 10px 30px;
        border-radius: 15px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .sign-in:hover {
        background-color: var(--highlight-darker-color);
    }
    
    .home_container {
        display: flex;
        justify-content: center;
        height: 600px;
        padding-top: 20px;
        background-color: var(--base-color); /* TODO: Might change */
    }
    
    .preview-box {
        width: 650px;
        height: 520px;
        background-color: var(--placeholder-color); /* TODO: Will change */
        border-radius: 20px;
        margin-right: 5%;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        background: url('../assets/Images/Comparison.png');
        background-position: center;
        background-size: cover;
    }
    
    .description {
        height: 520px;
        max-width: 400px; /* TODO: Might change */
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .description h1 {
        font-size: 26px;
        color: var(--black-color); /* TODO: Might change */
        line-height: 48px;
    }
    
    .description h1 span {
        font-weight: 700;
        font-size: 28px;
        font-family: 'Comic Sans MS', 'Comic Neue', 'EMcomic', 'Geneva', 'Verdana', sans-serif;
    }
    
    .description p {
        margin: 40px 0;
        color: var(--black-color); /* TODO: Might change */
        line-height: 36px;
        font-size: 18px;
    }
    
    .try-now {
        background-color: var(--highlight-color); /* TODO: Might change */
        color: var(--white-color); /* TODO: Might change */
        font-size: 18px;
        border: none;
        padding: 20px 30px; /* TODO: Might change */
        border-radius: 15px 15px 115px 115px; /* TODO: Might change */
        cursor: pointer;
        width: 80%;
        transition: background-color 0.3s ease;
        text-decoration: none;
    }
    .try-now:hover {
        background-color: var(--highlight-darker-color);
    }

    /************ WHY US PAGE SECTION ************/

    .why_us {
        background-color: var(--base-lighter-color);
        padding: 60px 20px; /* TODO: Might change */
        text-align: center;
    }

    .why_us h2 {
        font-size: 32px;
        color: var(--highlight-color);
        margin-bottom: 50px;
    }

    .cards {
        display: flex;
        justify-content: center;
        gap: 2%;
    }

    .card {
        background-color: var(--highlight-color);
        color: var(--white-color);
        padding: 50px 45px 50px 45px;
        border-radius: 20px;
        max-width: 320px;
        text-align: center;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        transition: transform 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card:nth-child(1) {
        margin-top: 50px;
    }
    .card:nth-child(2) {
        margin-top: 0;
    }
    .card:nth-child(3) {
        margin-top: 100px;
    }

    .card:hover {
        transform: translateY(-10px);
    }

    .icon {
        width: 40%;
        height: auto;
        margin-bottom: 25px;
    }

    .card h3 {
        font-size: 22px;
        margin-bottom: 25px;
    }

    .card p {
        font-size: 17px;
        line-height: 32px;
        color: var(--off-white-color);
    }

    /************ WALLPAPERS PAGE SECTION ************/
    .wallpapers_container {
        background-color: var(--base-color);
        padding: 60px 20px;
        text-align: center;
    }

    .wallpapers_container h2 {
        font-size: 28px;
        color: var(--highlight-color);
        margin-bottom: 40px;
    }

    .wallpapers_grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px 20px;
        justify-items: center;
    }

    .wallpaper {
        background-color: var(--placeholder-color);
        width: 100%;
        aspect-ratio: 2 / 3;
        border-radius: 15px;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    }
    .wallpaper:nth-child(2n) {
        margin-top: 20px;
    }

    /********** CONTACT FORM PAGE SECTION **********/
    .contact {
        background-color: var(--base-lighter-color);
        padding: 60px 20px;
        text-align: center;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    }

    .contact h2 {
        font-size: 28px;
        color: var(--highlight-color);
        margin-bottom: 20px;
        font-weight: 900;
    }

    .contact_form {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 40px;
        border-radius: 40px;
        box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.25), 0 4px 4px 0 rgba(0, 0, 0, 0.25) inset;
        border: 2px solid var(--highlight-color);
    }

    .contact_form label {
        font-size: 16px;
        color: var(--highlight-color);
        margin: 10px 0 5px;
        text-align: left;
        font-weight: 500;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 16px;
    }

    .contact_form input,
    .contact_form textarea {
        padding: 10px;
        font-size: 16px;
        border: 2px solid var(--highlight-color);
        border-radius: 10px;
        background-color: transparent;
        margin-bottom: 20px;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: 500;
        font-size: 16px;
    }
    .contact_form textarea {
        resize: none;
    }

    .contact_form input:focus,
    .contact_form textarea:focus {
        outline: none;
        border-color: var(--highlight-color);
    }

    .contact_form button {
        width: 50%;
        padding: 10px 20px;
        font-size: 16px;
        background-color: var(--highlight-color);
        color: var(--white-color);
        border: 2px solid var(--highlight-color);
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-right: 50%;
        transform: translateX(50%);
    }

    .contact_form button:hover {
        background-color: var(--highlight-darker-color);
        color: var(--white-color);
    }

    /********** FOOTER PAGE SECTION **********/
    .footer {
        background-color: var(--footer-color);
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 0 10px;
        height: 110px;
        width: 100%;
        font-size: 18px;
        color: var(--white-color);
    }


@media (width <= 1200px) {
    /***** LANDING HOME PAGE SECTION *****/
    .preview-box {
        width: 500px;
    }
    /***** WHY US PAGE SECTION *****/
    .card {
        width: 30%;
    }
}
@media (width <= 1000px) {
    /***** LANDING HOME PAGE SECTION *****/
    .preview-box {
        width: 450px;
    }
    .description {
        max-width: 300px;
    }
    .description p {
        margin: 20px 0;
    }
}
@media (width <= 850px) {
    /***** LANDING HOME PAGE SECTION *****/
    .home_container {
        flex-direction: column;
        height: auto;
        justify-content: left;
        align-items: center;
    }
    .preview-box {
        width: 650px;
        margin-right: 0;
    }
    .description {
        max-width: 650px;
        height: auto;
        margin: 40px 0 60px 0;
    }
    .description h1 {
        max-width: 400px;
    }
    .description p {
        margin: 30px 0;
    }
    .try-now {
        width: 90%;
    }
    /***** WHY US PAGE SECTION *****/
    .why_us h2 {
        margin-bottom: 40px;
    }
    .cards {
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        gap: 20px;
    }
    .card {
        max-width: none;
        width: 100%;
        flex-direction: row;
        gap: 40px;
    }
    .card:nth-child(1), .card:nth-child(2), .card:nth-child(3) {
        margin-top: 0;
    }
    .card:hover {
        transform: translateX(10px);
    }
    .icon {
        width: 80px !important; /* Necessary because inline styling used for the time icon */
        margin-bottom: 0;
    }
    .card_text {
        text-align: left;
        /* background-color: black; */
    }
    .card h3 {
        margin-bottom: 5px;
    }
    /***** WALLPAPERS PAGE SECTION *****/
    .wallpapers_grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .wallpaper:nth-child(n + 11) {
        display: none;
    }
}
@media (width <= 700px) {
    /***** LANDING HOME PAGE SECTION *****/
    .preview-box {
        width: 90%;
    }
    .description {
        max-width: 90%;
    }
    .nav_items {
        display: none;
    }
    /***** WHY US PAGE SECTION *****/
    .card h3 {
        margin-bottom: 15px;
    }
    /***** CONTACT FORM PAGE SECTION *****/
    .contact_form {
        padding: 30px 30px;
    }
}
@media (width <= 450px) {
    /***** LANDING HOME PAGE SECTION *****/
    .preview-box {
        height: 400px;
    }
    .sign-in {
        display: none;
    }
    /***** WHY US PAGE SECTION *****/
    .card {
        padding: 40px 25px;
    }
    .icon {
        width: 60px !important; /* Necessary because inline styling used for the time icon */
    }
    .card h3 {
        margin-bottom: 0;
    }
    .card p {
        display: none;
    }
    /***** WALLPAPERS PAGE SECTION *****/
    .wallpapers_grid {
        grid-template-columns: 1fr;
        gap: 10px;
    }
    .wallpaper {
        margin: 0 !important;
    }
    .wallpaper:nth-child(n + 7) {
        display: none;
    }
    /***** CONTACT FORM PAGE SECTION *****/
    .contact_form {
        border: none;
        box-shadow: none;
        margin: 0;
        padding: 0 20px;
    }
}

</style>
