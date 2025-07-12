<template>
    <main class="main_layout">
        <section :class="[{ main_area_expanded: isSidebarCollapsed, main_area: !isInRatio, main_area_2: isInRatio }]">
            <header :class="[{ main_title: !isInRatio, main_title_2: isInRatio }]">
                <router-link to="/" class="main_logo"><div></div></router-link>
                <nav class="navbar">
                    <button type="button" :class="[{ btn: !isInRatio, btn_2: isInRatio }]" style="display: none;">Sign out</button>
                    <svg
                        v-if="isSidebarCollapsed"
                        @click="toggleSidebar"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-chevron-left"
                        >
                        <polyline points="15 18 9 12 15 6"></polyline>
                    </svg>
                    <svg 
                        v-else
                        @click="toggleSidebar"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-chevron-right"
                        >
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </nav>
            </header>
            <div :class="[{ main_work_area: !isInRatio, main_work_area_2: isInRatio }]">
                <p :class="[{ step1: !isInRatio, step1_2: isInRatio }]"><span>Upload an image of your wall</span>: don't worry about objects on or surrounding the wall – we've got that covered.</p>
                <div :class="[{ upload_box: !isInRatio, upload_box_2: isInRatio }]">
                    <div v-if="loading" class="loading_overlay">
                        <span>Processing...</span>
                    </div>
                    <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" accept="image/jpeg, image/png">
                    <button type="button" class="upload_btn" :class="[{ btn: !isInRatio, btn_2: isInRatio }]" v-if="!fileUploaded" @click="openFileInput">Upload your wall</button>
                    <img v-if="imageUrl" :src="imageUrl" alt="Uploaded Image" class="uploaded_image" ref="image">
                    <div class="button_operation_container">
                        <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" v-if="fileUploaded" @click="openFileInput">New</button>
                        <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" v-if="fileUploaded && !imageCropped" @click="cropImage">Submit</button>
                    </div>
                </div>
                <div class="measurements_container">
                    <span>Wall Width: </span>
                    <input type="number" v-model="wallWidthFeet" placeholder="feet" :class="[{ measurements_input: !isInRatio, measurements_input_2: isInRatio }]">
                    <input type="number" v-model="wallWidthInches" placeholder="inch" :class="[{ measurements_input: !isInRatio, measurements_input_2: isInRatio }]">
                    <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" @click="handleWallWidthInput">Submit</button>
                </div>
                <div class="measurements_container">
                    <span>Roll Width: </span>
                    <input type="number" step="0.1" v-model="rollWidth" placeholder="inch" :class="[{ measurements_input: !isInRatio, measurements_input_2: isInRatio }]">
                    <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" @click="handleRollWidthInput">Submit</button>
                </div>
                <div class="measurements_container">
                    <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }, 'apply-button']" @click="applyWallpaper(this.selectedWallpaper)">Apply wallpaper</button>
                </div>
                <p :class="[{ step2: !isInRatio, step2_2: isInRatio }]">Choose a wallpaper, and watch your wall light up!</p>
                <p :class="[{ step1: !isInRatio, step1_2: isInRatio }]"><span class="custom_word">OPTIONAL - </span><span>Upload an image of your own wallpaper and match their pattern side-by-side!</span></p>
                <div class="upload_box">
                    <div v-if="wallpaperUploadLoading" class="loading_overlay">
                        <span>Processing...</span>
                    </div>
                    <input type="file" ref="wallpaperFileInput" @change="handleWallpaperFileUpload" style="display: none;" accept="image/jpeg, image/png">
                    <button type="button" class="upload_btn" :class="[{ btn: !isInRatio, btn_2: isInRatio }]" v-if="!wallpaperFileUploaded" @click="openWallpaperFileInput">Upload a wallpaper</button>
                    <div v-if="wallpaperImageUrl && !wallpaperShiftImage" class="" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;"><img :src="wallpaperImageUrl" alt="Uploaded Image" class="uploaded_image" ref="wallpaperImage"></div>
                    <div v-if="wallpaperShiftImage" class="" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;"><img :src="'data:image/jpeg;base64,' + wallpaperShiftImage" alt="Uploaded Image" class="uploaded_image" ref="wallpaperShiftImage"></div>
                    <div class="button_operation_container">
                        <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" v-if="wallpaperFileUploaded" @click="openWallpaperFileInput">New</button>
                        <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" v-if="wallpaperFileUploaded && !wallpaperImageCropped" @click="cropWallpaperImage">Submit</button>
                        <button type="button" :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }]" v-if="wallpaperImageCropped && !this.isWallpaperShiftingDone" @click="handleWallpaperShiftInput">Submit</button>
                        <button 
                            @mousedown="startShift(-this.wallpaperShiftPerClick)" 
                            @mouseup="stopShift"
                            @mouseleave="stopShift"
                            v-if="wallpaperImageCropped && !this.isWallpaperShiftingDone"
                            :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }, 'bg-green']">
                            Up ⬆️
                        </button>
                        <button 
                            @mousedown="startShift(this.wallpaperShiftPerClick)" 
                            @mouseup="stopShift" 
                            @mouseleave="stopShift"
                            v-if="wallpaperImageCropped && !this.isWallpaperShiftingDone"
                            :class="[{ upload_btn_small: !isInRatio, btn: !isInRatio, upload_btn_small_2: isInRatio, btn_2: isInRatio }, 'bg-green']">
                            Down ⬇️
                        </button>
                    </div>
                </div>
            </div>
        </section>
        <section :class="['sidebar', { sidebar_collapsed: isSidebarCollapsed }]">
            <header :class="[{ sidebar_header: !isInRatio, sidebar_header_2: isInRatio }]">
                <p>Wallpapers</p>
            </header>
            <div :class="[{ all_wallpapers: !isInRatio, all_wallpapers_2: isInRatio }]">
                <div class="wallpaper" v-for="wallpaper in wallpapers" :key="wallpaper" @click="handleWallpaperChoiceInput(wallpaper)" :style="{ background: 'url(' + require(`@/assets/Wallpapers/${wallpaper}`) + ')', backgroundSize: 'cover' }" :class="{ 'selected_wallpaper': wallpaper === selectedWallpaper }"></div>
            </div>
        </section>
    </main>
</template>

<script>
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import axios from 'axios';
import _ from 'lodash';
import constants from '@/assets/constants.json'

export default {
    name: "BoxLayout",
    props: {
        isInRatio: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            isSidebarCollapsed: false,
            fileUploaded: false,
            imageUrl: null,
            cropper: null,
            imageCropped: false,
            croppedImageBase64: null,
            wallpapers: constants.ALL_WALLPAPERS,
            loading: false,
            selectedWallpaper: null,
            wallWidthFeet: null,
            wallWidthInches: null,
            rollWidth: 21,

            wallpaperUploadLoading: null,
            wallpaperFileUploaded: false,
            wallpaperImageUrl: null,
            wallpaperCropper: null,
            wallpaperImageCropped: false,
            wallpaperCroppedImageBase64: null,
            wallpaperShiftImage: null,
            wallpaperShiftValue: 0,
            shiftInterval: null,
            isWallpaperShiftingDone: false,
            wallpaperShiftPerClick: 1,
            
            constants
        };
    },
    methods: {
        toggleSidebar() {
            this.isSidebarCollapsed = !this.isSidebarCollapsed;
        },
        handleWallWidthInput() {
            const feet = this.wallWidthFeet;
            const inches = this.wallWidthInches;
            if (!isNaN(feet) && !isNaN(inches) && feet !== null && inches !== null && feet >= 0 && inches >= 0 && inches <= 11 && feet <= 30 && !(feet === 0 && inches === 0)) {
                this.wallWidthFeet = feet;
                this.wallWidthInches = inches;
                console.log(constants.WALL_WIDTH_INPUT_SUCCESS_MSG);
                if (this.croppedImageBase64 && this.selectedWallpaper && this.rollWidth && this.isWallpaperShiftingDone) {
                    this.applyWallpaper(this.selectedWallpaper);
                }
            } else {
                this.wallWidthFeet = null;
                this.wallWidthInches = null;
                alert(constants.WALL_WIDTH_INPUT_ERR_MSG);
            }
        },
        handleRollWidthInput() {
            if (!isNaN(this.rollWidth) && this.rollWidth !== null && this.rollWidth > 0 && this.rollWidth <= constants.ROLL_WIDTH_CAP) {
                console.log(constants.ROLL_WIDTH_INPUT_SUCCESS_MSG);
                if (this.croppedImageBase64 && this.selectedWallpaper && this.wallWidthFeet && this.wallWidthInches && this.isWallpaperShiftingDone) {
                    this.applyWallpaper(this.selectedWallpaper);
                }
            } else {
                this.rollWidth = null;
                alert(constants.ROLL_WIDTH_INPUT_ERR_MSG);
            }
        },
        handleWallpaperChoiceInput(wallpaper) {
            this.selectedWallpaper = wallpaper;
            this.wallpaperShiftValue = 0;
            this.isWallpaperShiftingDone = true;
            console.log(constants.WALLPAPER_CHOICE_INPUT_SUCCESS_MSG)
            if (this.croppedImageBase64 && this.wallWidthFeet && this.wallWidthInches && this.rollWidth && this.isWallpaperShiftingDone) {
                this.applyWallpaper(this.selectedWallpaper);
            }
        },
        handleWallpaperShiftInput() {
            this.isWallpaperShiftingDone = true;
            console.log(constants.WALLPAPER_SHIFT_INPUT_SUCCESS_MSG)
            if (this.croppedImageBase64 && this.wallWidthFeet && this.wallWidthInches && this.rollWidth && this.selectedWallpaper) {
                this.applyWallpaper(this.selectedWallpaper);
            }
        },
        openFileInput() {
            this.$refs.fileInput.value = null;
            this.$refs.fileInput.click();
        },
        openWallpaperFileInput() {
            this.$refs.wallpaperFileInput.value = null;
            this.$refs.wallpaperFileInput.click();
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.imageUrl = URL.createObjectURL(file);
                this.fileUploaded = true;
                this.imageCropped = false;
                this.$nextTick(() => {
                    this.initializeCropper();
                });
            } else {
                this.fileUploaded = false;
                this.imageUrl = null;
                this.imageCropped = false;
            }
        },
        handleWallpaperFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.wallpaperImageUrl = URL.createObjectURL(file);
                this.wallpaperFileUploaded = true;
                this.wallpaperCropper = null;
                this.wallpaperImageCropped = false;
                this.wallpaperCroppedImageBase64 = null;
                this.wallpaperShiftImage = null;
                this.isWallpaperShiftingDone = false;
                this.wallpaperShiftValue = 0;
                this.$nextTick(() => {
                    this.initializeWallpaperCropper();
                });
            } else {
                this.wallpaperFileUploaded = false;
                this.wallpaperImageUrl = null;
                this.wallpaperImageCropped = false;
            }
        },
        initializeCropper() {
            if (this.cropper) {
                this.cropper.destroy();
            }
            if (!this.imageCropped) {
                this.cropper = new Cropper(this.$refs.image, {
                    viewMode: 1,
                    responsive: true,
                    autoCropArea: 0.8
                    // aspectRatio: 16 / 9
                });
            }
        },
        initializeWallpaperCropper() {
            if (this.wallpaperCropper) {
                this.wallpaperCropper.destroy();
                this.wallpaperCropper = null;
            }
            if (!this.wallpaperImageCropped) {
                this.wallpaperCropper = new Cropper(this.$refs.wallpaperImage, {
                    viewMode: 2,
                    responsive: true,
                    autoCropArea: 1
                    // aspectRatio: 16 / 9
                });
            }
        },
        blobToBase64(blob) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = () => resolve(reader.result);
                reader.onerror = error => reject(error);
            });
        },
        async cropImage() {
            if (this.cropper) {
                const canvas = this.cropper.getCroppedCanvas();
                this.loading = true;
                const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
                const base64Image = await this.blobToBase64(blob);
                this.croppedImageBase64 = base64Image;
                this.imageUrl = canvas.toDataURL('image/jpeg');
                this.cropper.destroy();
                this.cropper = null;
                this.imageCropped = true;
                await this.uploadCroppedImage(this.croppedImageBase64);
                await this.initializePreview();
                if (this.croppedImageBase64 && this.wallWidthFeet && this.wallWidthInches && this.rollWidth && this.selectedWallpaper && this.isWallpaperShiftingDone) {
                    this.applyWallpaper(this.selectedWallpaper);
                }
                this.loading = false;
            }
        },
        async cropWallpaperImage() {
            if (this.wallpaperCropper) {
                const canvas = this.wallpaperCropper.getCroppedCanvas();
                this.wallpaperLoading = true;
                const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
                const base64Image = await this.blobToBase64(blob);
                this.wallpaperCroppedImageBase64 = base64Image;
                this.wallpaperImageUrl = canvas.toDataURL('image/jpeg');
                this.wallpaperCropper.destroy();
                this.wallpaperCropper = null;
                this.wallpaperImageCropped = true;
                await this.uploadWallpaperCroppedImage(this.wallpaperCroppedImageBase64);
                this.wallpaperLoading = false;
                if (this.croppedImageBase64 && this.wallWidthFeet && this.wallWidthInches && this.rollWidth && this.selectedWallpaper && this.isWallpaperShiftingDone) {
                    this.applyWallpaper(this.selectedWallpaper);
                }
            }
        },
        async uploadCroppedImage(base64Image) {
            try {
                const response = await axios.post(`${constants.API_URL}/upload`, { image: base64Image }, { headers: {
                    'Content-Type': 'application/json'
                } });
                if (response.data === true) {
                    console.log(constants.UPLOAD_SUCCESS_MSG);
                } else {
                    console.error(constants.UPLOAD_ERR_MSG);
                    alert(constants.UPLOAD_ERR_MSG);
                    this.fileUploaded = false;
                    this.imageUrl = null;
                    this.croppedImageBase64 = null;
                    this.imageCropped = false;
                    if (this.cropper) {
                        this.cropper.destroy();
                        this.cropper = null;
                    }
                    this.$refs.fileInput.value = null;
                }
            } catch (error) {
                console.error('Error uploading image:', error);
                alert(constants.UPLOAD_ERR_MSG);
                this.fileUploaded = false;
                this.imageUrl = null;
                this.croppedImageBase64 = null;
                this.imageCropped = false;
                if (this.cropper) {
                    this.cropper.destroy();
                    this.cropper = null;
                }
                this.$refs.fileInput.value = null;
            }
        },
        async uploadWallpaperCroppedImage(base64Image) {
            try {
                const response = await axios.post(`${constants.API_URL}/wallpaper-upload`, { image: base64Image }, { headers: {
                    'Content-Type': 'application/json'
                } });
                if (response.data === true) {
                    console.log(constants.UPLOAD_SUCCESS_MSG);
                    this.selectedWallpaper = constants.CUSTOM_WALLPAPER_NAME;
                    console.log(constants.WALLPAPER_CHOICE_INPUT_SUCCESS_MSG)
                    try {
                        const response = await axios.post('http://localhost:8000/wallpaper-preview-initialize');
                        this.wallpaperShiftImage = response.data.image;
                        this.wallpaperShiftPerClick = Math.ceil(0.005 * response.data.height);
                        // TODO: Maybe keep the shift value to 0.5% of height of image.
                    } catch (error) {
                        console.error("Error initializing preview: ", error)
                        alert("Error initializing preview: ", error)
                    }

                } else {
                    console.error(constants.UPLOAD_ERR_MSG);
                    alert(constants.UPLOAD_ERR_MSG);
                    this.wallpaperFileUploaded = false;
                    this.wallpaperImageUrl = null;
                    this.wallpaperCroppedImageBase64 = null;
                    this.wallpaperImageCropped = false;
                    if (this.wallpaperCropper) {
                        this.wallpaperCropper.destroy();
                        this.wallpaperCropper = null;
                    }
                    this.$refs.wallpaperFileInput.value = null;
                }
            } catch (error) {
                console.error('Error uploading image:', error);
                alert(constants.UPLOAD_ERR_MSG);
                this.wallpaperFileUploaded = false;
                this.wallpaperImageUrl = null;
                this.wallpaperCroppedImageBase64 = null;
                this.wallpaperImageCropped = false;
                if (this.wallpaperCropper) {
                    this.wallpaperCropper.destroy();
                    this.wallpaperCropper = null;
                }
                this.$refs.wallpaperFileInput.value = null;
            }
        },
        // async adjustImageShift() {
        //     try {
        //         const response = await axios.post('http://localhost:8000/wallpaper-preview-adjust', { shift: this.wallpaperShiftValue });
        //         this.wallpaperShiftImage = response.data.image;
        //     } catch (error) {
        //         console.error("Error adjusting preview:", error);
        //     }
        // },
        throttleAdjustImageShift: _.throttle(async function() {
            try {
                const response = await axios.post('http://localhost:8000/wallpaper-preview-adjust', { shift: this.wallpaperShiftValue });
                this.wallpaperShiftImage = response.data.image;
            } catch (error) {
                console.error("Error adjusting preview:", error);
            }
        }, 200), // Adjust the throttle delay as needed
        startShift(direction) {
            this.shiftDirection = direction;
            this.shiftInterval = setInterval(() => {
                this.wallpaperShiftValue += this.shiftDirection;
                this.throttleAdjustImageShift();
            }, 50); // Adjust the interval time as needed
        },
        stopShift() {
            clearInterval(this.shiftInterval);
            this.shiftInterval = null;
        },
        async initializePreview() {
            try {
                const response = await axios.post(`${constants.API_URL}/initialize`, { image_path: 'cropped_image.jpg' })
                if (response.data === true) {
                    console.log(constants.WALL_DETECTION_SUCCESS_MSG)
                } else {
                    console.error(constants.WALL_DETECTION_ERR_MSG);
                    alert(constants.WALL_DETECTION_ERR_MSG);
                    this.fileUploaded = false;
                    this.imageUrl = null;
                    this.imageCropped = false;
                    this.croppedImageBase64 = null;
                    if (this.cropper) {
                        this.cropper.destroy();
                        this.cropper = null;
                    }
                    this.loading = false;
                }
            } catch (error) {
                console.error('Error uploading image:', error);
                alert(constants.UNKNOWN_ERR_MSG);
                this.fileUploaded = false;
                this.imageUrl = null;
                this.imageCropped = false;
                this.croppedImageBase64 = null;
                if (this.cropper) {
                    this.cropper.destroy();
                    this.cropper = null;
                }
                this.loading = false;
            }
        },
        async applyWallpaper(wallpaper) {
            if (!this.croppedImageBase64) {
                alert(constants.APPLY_BEFORE_UPLOAD_ERR_MSG);
                return;
            }

            else if (isNaN(this.wallWidthFeet) || this.wallWidthFeet < 0 || isNaN(this.wallWidthInches) || this.wallWidthInches < 0 || this.wallWidthInches >= 12 || this.wallWidthFeet === null || this.wallWidthInches === null || (this.wallWidthFeet === 0 && this.wallWidthInches === 0)) {
                alert(constants.APPLY_BEFORE_WALL_WIDTH_ERR_MSG)
                return;
            }

            else if (isNaN(this.rollWidth) || this.rollWidth < 0 || this.rollWidth > constants.ROLL_WIDTH_CAP || this.rollWidth === null) {
                alert(constants.APPLY_BEFORE_ROLL_WIDTH_ERR_MSG);
                return;
            }

            else if (!this.selectedWallpaper) {
                alert(constants.APPLY_BEFORE_WALLPAPER_CHOICE_ERR_MSG);
                return;
            }

            else if (!this.isWallpaperShiftingDone) {
                alert(constants.APPLY_BEFORE_SHIFT_INPUT_ERR_MSG);
                return;
            }
            
            this.loading = true;
            this.selectedWallpaper = wallpaper;
            try {
                const finalWallWidth = (this.wallWidthFeet * 12) + this.wallWidthInches
                const response = await axios.post(`${constants.API_URL}/apply`, { image_path: 'cropped_image.jpg', wallpaper_path: wallpaper, wall_width: finalWallWidth, roll_width: this.rollWidth, best_shift: this.wallpaperShiftValue});
                if (response.data !== false) {
                    console.log(constants.WALLPAPER_APPLY_SUCCESS_MSG);
                    const base64Img = response.data.image;
                    const dataUrl = `data:image/jpeg;base64,${base64Img}`;
                    this.imageUrl = dataUrl;
                } else {
                    console.error(response.WALLPAPER_APPLY_ERR_MSG);
                    alert(constants.WALLPAPER_APPLY_ERR_MSG);
                }
            } catch (error) {
                console.error('Error applying wallpaper:', error);
                alert(constants.WALLPAPER_APPLY_ERR_MSG);
            } finally {
                this.loading = false;
            }
        }
    },
    watch: {
        imageUrl(newValue, oldValue) {
            if (newValue && !oldValue) {
                window.addEventListener('resize', this.initializeCropper);
            } else if (!newValue && oldValue) {
                window.removeEventListener('resize', this.initializeCropper);
            }
        },
        wallpaperImageUrl(newValue, oldValue) {
            if (newValue && !oldValue) {
                window.addEventListener('resize', this.initializeWallpaperCropper);
            } else if (!newValue && oldValue) {
                window.removeEventListener('resize', this.initializeWallpaperCropper);
            }
        }
    }
};
</script>


<style>
    :root {
        --main-color: #e0eee0;
        --sidebar-color: #d0ddd0;
        --highlight-color: #12664f;
        --black-color: black;
        --white-color: white;

        --green-color: rgb(0, 120, 0);
        --red-color: rgb(220, 0, 0);

        --base-font-size: calc(12px + 0.5vw); /* Responsive font size */
        --header-height: calc(10% + 1vw); /* Responsive header height */

        --main-layout-height: 1800px;
        --sidebar-width: 25%;
        --main-area-width: 75%;
        /* --upload-box-height: 38%; */
        --upload-box-height: 600px;
        --upload-box-width: 65%;
        --normal-header-height: 7%;
    }

    * {
        box-sizing: border-box;
        font-family: Avenir, 'Helvetica';
        margin: 0;
        padding: 0;
    }

    .bg-green {
        background-color: var(--highlight-color) !important;
    }

    .btn {
        background-color: var(--black-color);
        color: var(--white-color);
        font-size: 16px;
        border: none;
        width: auto;
        height: auto;
        padding: 10px 30px;
        border-radius: 15px;
        margin: 0;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .apply-button {
        background-color: var(--highlight-color) !important;
        font-size: 16px !important;
        margin: 15px 0 !important;
        padding: 10px 10% !important;
    }
    
    /* For isInRatio - DONE */
    .btn_2 {
        font-size: var(--base-font-size);
        padding: calc(0.5em + 0.2vw) calc(1.5em + 0.5vw);

        background-color: var(--black-color);
        color: var(--white-color);
        border: none;
        width: auto;
        height: auto;
        border-radius: 15px;
        margin: 0;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .main_layout {
        background-color: var(--main-color);
        min-height: var(--main-layout-height);
        height: 100vh;
        width: 100vw;
        border: 1px solid var(--black-color);
        display: flex;
        overflow: hidden;
        scrollbar-width: none;
    }
    .main_layout::-webkit-scrollbar {
        display: none;
    }

    .measurements_container {
        display: flex;
        width: 100%;
        background-color: transparent;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-top: 15px;
    }

    .measurements_input {
        padding: 10px;
        width: 15%;
        max-width: 100px;
        font-size: 14px;
        border: 2px solid var(--highlight-color);
        box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
        border-radius: 10px;
        background: transparent;
        outline: none;
    }

    .measurements_input_2 {
        /* margin-top: 1rem; */
        padding: calc(0.5em + 0.2vw) calc(1.5em + 0.5vw);
        border-radius: 10px;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
        border: 2px solid var(--highlight-color);
        font-size: 1rem;
        width: 40%;
        background: transparent;
        outline: none;
    }


    input[type=number]::-webkit-outer-spin-button,
    input[type=number]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type=number] {
        -moz-appearance: textfield;
    }

    .main_area {
        width: var(--main-area-width);
        height: 95%;
        transition: all 0.3s;
        scrollbar-width: none;
    }
    .main_area::webkit-scrollbar {
        display: none;
    }

    /* For isInRatio - DONE */
    .main_area_2 {
        width: var(--main-area-width);

        height: 100%;
        transition: all 0.3s;
        scrollbar-width: none;
    }
    .main_area_2::webkit-scrollbar {
        display: none;
    }

    .main_area_expanded {
        width: 100%;
        transition: all 0.3s;
    }

    .main_title {
        width: 100%;
        height: var(--normal-header-height);
        background-color: var(--main-color);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0% 5%;
    }

    /* For isInRatio - DONE */
    .main_title_2 {
        height: var(--header-height);

        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0% 5%;
    }

    .main_logo {
        all: unset;
        cursor: pointer
    }
    .main_logo:visited {
        all: unset;
    }
    
    .main_logo div {
        background: url('../assets/logo.png');
        width: 162px;
        height: 80px;
        background-position: center;
        background-size: cover;
        filter: hue-rotate(100deg) brightness(0.5) contrast(1.2);
    }

    .main_title span {
        font-family: 'Comic Sans MS', 'Comic Neue', 'EMcomic', 'Geneva', 'Verdana', sans-serif;
        font-size: 28px;
        font-weight: 700;
    }

    /* For isInRatio - DONE */
    .main_title_2 span {
        font-size: calc(var(--base-font-size) * 1.75);
        
        font-family: 'Comic Sans MS', 'Comic Neue', 'EMcomic', 'Geneva', 'Verdana', sans-serif;
        font-weight: 700;
    }

    .navbar {
        display: flex;
        width: 100%;
        justify-content: right;
        align-items: center;
        gap: 0px;
    }

    .main_title svg {
        color: var(--black-color);
        margin-left: 20px;
        cursor: pointer;
    }

    /* For isInRatio - DONE */
    .main_title_2 svg {
        color: var(--black-color);
        margin-left: 20px;
        cursor: pointer;
    }


    .main_work_area {
        width: 100%;
        height: calc(100% - var(--normal-header-height));
    }

    /* For isInRatio - DONE */
    .main_work_area_2 {
        height: calc(100% - var(--header-height));

        width: 100%;
    }

    .step1 {
        font-size: 18px;
        color: var(--black-color);
        margin: 0 0 2% 0;
        padding: 10px 4% 0 4%;
        line-height: 32px;
    }

    /* For isInRatio - DONE */
    .step1_2 {
        font-size: var(--base-font-size);
        padding: calc(1em + 0.5vw) 4%;

        color: var(--black-color);
        margin: 0;
        line-height: 32px;
    }

    .step1 span, .step2 {
        font-weight: 700;
        color: var(--black-color);
        font-size: 20px;
    }

    /* For isInRatio - DONE */
    .step1_2 span, .step2_2 {
        font-size: calc(var(--base-font-size) * 1.25);

        font-weight: 700;
        color: var(--black-color);
    }

    .step2 {
        padding: 2% 4% 10px 4%;
        line-height: 32px;
    }

    /* For isInRatio - DONE */
    .step2_2 {
        padding: calc(1em + 0.5vw) 4%;
        line-height: 1.5em;
    }
    .custom_word {
        font-size: 24px !important;
        color: var(--highlight-color) !important;
    }

    .upload_box {
        position: relative;
        width: var(--upload-box-width);
        height: var(--upload-box-height);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        margin-left: 50%;
        transform: translate(-50%);
        overflow: hidden;
        border: 2px solid var(--highlight-color);
        /* padding: 5%; */
    }

    /* For isInRatio - DONE */
    .upload_box_2 {
        margin-bottom: calc(1em + 1vw);

        position: relative;
        width: var(--upload-box-width);
        height: var(--upload-box-height);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        margin-left: 50%;
        transform: translate(-50%);
        overflow: hidden;
        border: 2px solid var(--highlight-color);
    }

    .loading_overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--white-color);
        font-size: 20px;
        z-index: 10;
    }

    .uploaded_image {
        max-width: calc(100% - 5%);
        max-height: calc(100% - 35.5px);
        object-fit: fill;
    }

    .button_operation_container {
        position: absolute;
        height: auto;
        bottom: 10px;
        background-color: transparent;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        /* align-items: center; */
        gap: 10px;
        padding: 0 10px;
    }

    .upload_btn_small {
        background-color: var(--black-color);
        color: var(--white-color);
        font-size: 14px;
        padding: 8px 20px;
        border-radius: 10px;
        box-shadow: var(--main-color) 0px 0px 2px;
        cursor: pointer;
    }

    /* For isInRatio - DONE */
    .upload_btn_small_2 {
        font-size: calc(var(--base-font-size) * 0.875);
        padding: calc(0.5em + 0.5vw) calc(1em + 0.5vw);

        background-color: var(--black-color);
        color: var(--white-color);
        border-radius: 10px;
        box-shadow: var(--main-color) 0px 0px 2px;
        cursor: pointer;
    }

    .sidebar {
        background-color: var(--sidebar-color);
        width: var(--sidebar-width);
        height: 100%;
        transition: all 0.3s;
    }

    .sidebar_collapsed {
        width: 0%;
        overflow: hidden;
        transition: all 0.3s;
    }

    .sidebar_header {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: var(--normal-header-height);
    }

    /* For isInRatio - DONE */
    .sidebar_header_2 {
        height: var(--header-height);

        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .sidebar_header p {
        margin-left: 7%;
        padding: 0 2% 7px 2%;
        font-size: 20px;
        border-bottom: 2px solid green;
    }

    /* For isInRatio - DONE */
    .sidebar_header_2 p {
        font-size: calc(var(--base-font-size) * 1.25);

        margin-left: 7%;
        padding: 0 2% 7px 2%;
        border-bottom: 2px solid green;
    }

    .sign-out-btn {
        margin-right: 4%;
    }

    .all_wallpapers {
        height: calc(100% - var(--normal-header-height));
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow-y: scroll;
        flex-shrink: 0;
        scrollbar-width: none;
    }
    .all_wallpapers::-webkit-scrollbar {
        display: none;
    }

    /* For isInRatio - DONE */
    .all_wallpapers_2 {
        height: calc(100% - var(--header-height));

        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow-y: scroll;
        flex-shrink: 0;
        scrollbar-width: none;
    }
    .all_wallpapers_2::-webkit-scrollbar {
        display: none;
    }

    .wallpaper {
        width: 75%;
        border: 1px solid var(--black-color);
        border-radius: 10px;
        flex-shrink: 0;
        margin-bottom: 20px;
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
        aspect-ratio: 2 / 3;
        background-size: contain;
        cursor: pointer;
        transition: all 0.5s ease-in-out;
    }

    .wallpaper.selected_wallpaper {
        border: 4px solid var(--highlight-color);
        /* box-sizing: content-box; */
        transition: all 0.5s ease-in-out;
    }

    @media (width <= 1340px) {
        :root {
            --main-layout-height: 1850px;
        }
        .upload_box {margin-bottom: 20px;}
    }
    @media (width <= 850px) {
        :root {
            --main-layout-height: 2000px;
            --upload-box-height: 33%;
        }
        .navbar svg {display: none;}
        .main_layout {
            flex-direction: column;
        }
        .main_area {
            width: 100%;
        }
        .step1 {
            margin-top: 0;
            padding-top: 0;
        }
        .step2 {
            margin-bottom: 10px;
            padding-bottom: 0;
        }
        .sidebar, .sidebar_collapsed {
            width: 100%;
            height: 350px;
            transition: width 0.3s;
            background-color: var(--sidebar-color);
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 10px;
            padding-top: 20px;
        }
        .sidebar_header {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .all_wallpapers {
            height: auto;
            display: flex;
            overflow-x: scroll;
            overflow-y: hidden;
            scrollbar-width: none; /* For Firefox */
            white-space: nowrap;
            padding: 5px;
            flex-direction: row;
            gap: 5px;
        }
        .all_wallpapers::-webkit-scrollbar {
            display: none; /* For Chrome, Safari, and Opera */
        }
        .wallpaper, .wallpaper_upload_box {
            width: 140px;
            height: 210px;
            background-color: transparent;
            margin-right: 10px;
            flex-shrink: 0;
        }
    }
    @media (width <= 600px) {
        :root {
            --main-layout-height: 2000px;
            --upload-box-height: 33%;
        }
        .step2, .step1 {
            margin: 10px 0 20px 0;
        }
    }
    @media (width <= 550px) {
        :root {
            --main-layout-height: 1950px;
            --upload-box-height: 31%;
        }
        .step2, .step1 {
            margin: 10px 0 20px 0;
        }
    }
    @media (width <= 500px) {
        :root {
            --main-layout-height: 2050px;
            --upload-box-height: 31%;
        }
        .step2, .step1 {
            margin: 10px 0 20px 0;
        }
    }
    @media (width <= 400px) {
        :root {
            --main-layout-height: 1950px;
            --upload-box-height: 29%;
        }
        .step2, .step1 {
            margin: 10px 0 20px 0;
        }
    }
    @media (width <= 350px) {
        :root {
            --main-layout-height: 2000px;
            --upload-box-height: 28%;
        }
        .step2, .step1 {
            margin: 10px 0 20px 0;
        }
    }
</style>

<!-- Works until 320px width -->
