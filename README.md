# VehicleSpawn-Names for FiveM
Same as the sirenId finder just a simple python made to extract vehName from the vehicle.meta files. Built by ai and edited by me from the sirenID extractor.

Place inside your main resource folder and right click inside the directory and open in terminal.

Once terminal is open type python vehName_extractor.py and hit enter.

The python script will run in terminal or powershell and set results in 2 .txt files.

One will be a simplified .txt containing all the modelName from all vehicle.meta files in your server. Great for having a collective list of spawn codes in a simple text document and saved locally or in your discord server.
The other will be a slightly more detailed showing you the folder name the modelName is in and the modelName as well. 

If you have one folder of vehicle files in your resources change line 9:

self.base_directories = ["emergency"]

to the folder name you need to search. Mine is labeled [emergency] so that is what I used.

Likewise if you have multiple folders in your resources you would like to check use line 201:

 directories_to_search = [ #if you have multiple vehilce folders put them here as they are typed in your resource folder.
    "[emergency]",
    "[Vehicles]",
]
And change or add as needed for the folders you have.

If you see anything that can be approved on submit a PR.
