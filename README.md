# NFTs Upload Properties to **existing** NFT Collection on Opensea

Hi all, I created my nft collection on Opensea using this: https://github.com/nftdevs/NFTs-Upload-to-OpenSea. At the time, they did not have the function to upload properties. Now they do: https://github.com/nftdevs/NFTs_Upload_To_OpenSea_With_Metadata. 

Use this if you are hoping to edit an existing collection to add properties. Use something else if you are *creating* a new collection.

If you are like me and already created a collection without properties, you may want to go back and update the properties via an automated approach. I wasn't able to find one that did, so I tweaked the existing code of the original app that I used. See below for credits.  

Please REVIEW the code prior to using. Any suggestions would be much appreciated (see search function in code). 

I tweaked this code for my own project so you **WILL** need to tweak it for yours (**see step 6 below**). It's not the best as I'm not savvy in coding. Also, it uses the search function to look for the existing NFT and Opensea's search function isn't the best. Nonetheless, it was a struggle for me to find anything that worked so hopefully this is a good start for you. If you are using this, my assumption is that you have some basic knowledge in coding. Main concept of this is that you input which NFT you want to edit, the program will then search for that number, click on it to edit and add properties.  

This only works for json files.

➜ **Feel free to provide feedback on how to improve the code**: <br>
➜ **0x083eCd0020ce2972e7A8a418C37F8e91f9a9fAdF** (Ethereum).<br>
➜ **Check out my collection on OpenSea: https://opensea.io/collection/piggieland**. I'll likely take any offers :)<br>

Steps:
1. Download Python and Chrome browser
2. Make sure you have the correct ChromeDriver in folder
3. Run Command Prompt
4. cd to correct directory
5. Input 'pip install -r requirements.txt'
6. **Edit 'python uploadproperties.py' prior to running. You will need to edit the alt name under the Search function for the program to select the appropriate image. Please test this program prior to looping through multiple images**
7. Press the "Open Chrome Browser" button
8. Set up your metamask wallet and login to Opensea using your wallet. Once you are signed in, you should not have to login again while the script runs. You will need to login in order for the program to work.
9. Open the collection you want to edit. Copy collection link and paste it in app.
10. Edit Start and End number to the NFTs that you want to edit. Edit other parameters as needed.
11. Review 'python uploadproperties.py' as needed to make sure the code is up to date with your parameters.
10. Click Start button

Credits @nftdevs

*Never give out your Metamask wallet information.  
