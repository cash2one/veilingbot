# Veilingbot
This is my dear old veilingbot (auction bot) hobby project. 
It has scored me some nice hot spa and sushi restaurant discount codes.
I stopped using it a while ago, so here's the source code. 

## Usage

```bash
sudo apt-get install git python-pip tmux htop libfontconfig1 
git clone <repo url>
cd veilingbot
pip install -r requirements.txt
```
Also, install phantomjs and place it in the project root. 

Add hosts like facebook to hostsfile to speed up browser starts and decrease bandwidth usage

    127.0.1.2       connect.facebook.com facebook.com www.facebook.com
    127.0.1.5       apis.google.com google-analytics.com www.google-analytics.com plus.google.com
    #127.0.1.3      cdn1.vakantieveilingen.nl cdn2.vakantieveilingen.nl cdn3.vakantieveilingen.nl cdn4.vakantieveilingen.nl
    #127.0.1.4      static1.vakantieveilingen.nl static2.vakantieveilingen.nl static3.vakantieveilingen.nl static4.vakantieveilingen.nl

