# Exercise 1: Running containers

In this exercise, we'll learn the basics of pulling images, starting, stopping, and removing containers.

### Pulling an image

To run containers, we'll first need to pull some images.

1. Let's see what images we have currently on our machine, by running `docker images`:

    ```
    artur@Artur-PC:~/Desktop/PROJECTS/materials-about-containerized-applications$ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ```
    >:exclamation: **Wymagany screenshot 01!**

2. On a fresh Docker installation, we should have no images. Let's pull one from Dockerhub.

    We usually pull images from DockerHub by tag. These look like:

    ```
    # Official Docker images
    <repo>:<tag>
    # ubuntu:22.04
    # elasticsearch:8.15.1
    # nginx:latest

    # User or organization made images
    <user or org>/<repo>:<tag>
    # delner/ubuntu:16.04
    # bitnami/rails:latest
    ```

    We can search for images using `docker search <keyword>`

    ```
    $ docker search ubuntu
    NAME                             DESCRIPTION                                     STARS     OFFICIAL
    ubuntu                           Ubuntu is a Debian-based Linux operating sys…   17252     [OK]
    ubuntu/chiselled-jre             [MOVED TO ubuntu/jre] Chiselled JRE: distrol…   3         
    ubuntu/python                    A chiselled Ubuntu rock with the Python runt…   12        
    ubuntu/mimir                     Ubuntu ROCK for Mimir, a horizontally scalab…   0         
    ubuntu/dotnet-deps               Chiselled Ubuntu for self-contained .NET & A…   16        
    ubuntu/dotnet-aspnet             Chiselled Ubuntu runtime image for ASP.NET a…   22        
    ```
    >:exclamation: **Wymagany screenshot 02!**

    You can also find images online at [DockerHub](https://hub.docker.com/).

    Run `docker pull ubuntu:22.04` to pull an image of Ubuntu 22.04 from DockerHub.

    ```
    $ docker pull ubuntu:22:04
    22.04: Pulling from library/ubuntu
    857cc8cb19c0: Pull complete 
    Digest: sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658
    Status: Downloaded newer image for ubuntu:22.04
    docker.io/library/ubuntu:22.04
    ```  
    >:exclamation: **Wymagany screenshot 03!**

3. We can also pull different versions on the same image.

    Run `docker pull ubuntu:22.10` to pull an image of Ubuntu 22.10.

    ```
    22.10: Pulling from library/ubuntu
    3ad6ea492c35: Pull complete 
    Digest: sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489
    Status: Downloaded newer image for ubuntu:22.10
    docker.io/library/ubuntu:22.10
    ```
    >:exclamation: **Wymagany screenshot 04!**
    
    Then, when we run `docker images again, we should get:

    ```
    REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
    ubuntu       22.04     53a843653cbc   4 weeks ago     77.9MB
    ubuntu       22.10     692eb4a905c0   14 months ago   70.3MB
    ```
    >:exclamation: **Wymagany screenshot 05!**

4.  Over time, your machine can collect a lot of images, so it's nice to remove unwanted images.
    Run `docker rmi <IMAGE ID>` to remove the Ubuntu 22.10 image we won't be using.

    ```
    $ docker rmi 692eb4a905c0
    Untagged: ubuntu:22.10
    Untagged: ubuntu@sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489
    Deleted: sha256:692eb4a905c074054e0a35d647671f0e32ed150d15b23fd7bc745cfb2fdeddbd
    Deleted: sha256:1e8bb0620308641104e68d66f65c1e51de68d7df7240b8a99a251338631c6911
    ```
    >:exclamation: **Wymagany screenshot 06!**

    Alternatively, you can delete images by tag or by a partial image ID. In the previous example, the following would have been equivalent:  
     - `docker rmi 69`
     - `docker rmi ubuntu:22.10`

    Running `docker images` should reflect the deleted image.

    ```
    $ docker images
    REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
    ubuntu       22.04     53a843653cbc   4 weeks ago   77.9MB
    ```
    >:exclamation: **Wymagany screenshot 07!**

    Skrót do usuwania wszystkich obrazów z systemu to `docker rmi $(docker images -a -q)`
    ```
    $ docker rmi $(docker images -a -q)
    Untagged: ubuntu:22.04
    Untagged: ubuntu@sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658
    Deleted: sha256:53a843653cbcd9e10be207e951d907dc2481d9c222de57d24cfcac32e5165188
    Deleted: sha256:1b9b7346fee7abbc7f5538eaa23548bd05a45abe8daf6794024be0c8ad7d60bb
    ```
    >:exclamation: **Wymagany screenshot 08!**

### Running our container

Using the Ubuntu 16.04 image we downloaded, we can run a first container. Unlike a traditional virtualization framework like VirtualBox or VMWare, we can't just start a virtual machine running this image without anything else: we have to give it a command to run.

The command can be anything you want, as long as it exists on the image. In the case of the Ubuntu image, it's a Linux kernel with many of the typical applications you'd find in a basic Linux environment.

1.  Let's do a very simple example. Run `docker run ubuntu:22.04 /bin/echo 'Hello world!'`
    If we removed images earlier, it will be pulledagain.

    ```
    $ docker run ubuntu:22.04 /bin/echo 'Hello world!'
    Unable to find image 'ubuntu:22.04' locally
    22.04: Pulling from library/ubuntu
    857cc8cb19c0: Pull complete 
    Digest: sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658
    Status: Downloaded newer image for ubuntu:22.04
    Hello world!
    ```
    >:exclamation: **Wymagany screenshot 09!**

    The `/bin/echo` command is a really simple application that just prints whatever you give it to the terminal. 
    We passed it 'Hello world!', so it prints `Hello world!` to the terminal.

    When you run the whole `docker run` command, it creates a new container from the image specified, then runs the command inside the container. 
    From the previous example, the Docker container started, then ran the `/bin/echo` command in the container.  

2. Let's check what containers we have after running this. Run `docker ps`:  

    ```
    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    ```
    >:exclamation: **Wymagany screenshot 10!**

    That's strange: no containers right? 
    The `ps` command doesn't show stopped containers by default, add the `-a` flag.

    ```
    $ docker ps -a
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                      PORTS     NAMES
    7ed5e2746181   ubuntu:22.04   "/bin/echo 'Hello wo…"   18 minutes ago   Exited (0) 18 minutes ago             heuristic_bhaskara
    ```  
   
    >:exclamation: **Wymagany screenshot 11!**

    Okay, there's our container. But why is the status "Exited"?  
    Documentation says:  *Docker containers only run as long as the command it starts with is running.*  
    In our example, it ran `/bin/echo` successfully, printed some output, then exited with status code 0 (which means no errors).  
    When Docker saw this command exit, the container stopped.  


3. Let's do something a bit more interactive. Run `docker run ubuntu:22.04 /bin/bash`

    ```
    $ docker run ubuntu:22.04 /bin/bash
    $
    ```
    >:exclamation: **Wymagany screenshot 12!**

    Notice nothing happened. When we run `docker ps -a`:  

    ```
    $ docker ps -a
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                      PORTS     NAMES
    8ce9e62ee76c   ubuntu:22.04   "/bin/bash"              15 seconds ago   Exited (0) 15 seconds ago             gifted_jemison
    7ed5e2746181   ubuntu:22.04   "/bin/echo 'Hello wo…"   25 minutes ago   Exited (0) 25 minutes ago             heuristic_bhaskara
    ```
    >:exclamation: **Wymagany screenshot 13!**

    The container exited instantly. Why? We were running the `/bin/bash` command, which is an interactive program. 
    However, the `docker run` command doesn't run interactively by default, therefore the `/bin/bash` command exited, and the container stopped.

    Instead, let's add the `-it` flags, which tells Docker to run the command interactively with your terminal.

    ```
    $ docker run -it ubuntu:22.04 /bin/bash
    root@94ff3d83e360:/# 
    ```
    >:exclamation: **Wymagany screenshot 14!**

    This looks a lot better. This means you're in a BASH session inside the Ubuntu container. 
    Notice you're running as `root` and the container ID that follows.  
    You can now use this like a normal Linux shell. Try `pwd` and `ls` to look at the file system.  

    ```
    root@94ff3d83e360:/# pwd
    /
    root@94ff3d83e360:/# ls
    bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
    ```
    >:exclamation: **Wymagany screenshot 15!**

    You can type `exit` to end the BASH session, terminating the command and stopping the container.

    ```
    root@94ff3d83e360:/# exit
    exit
    $
    ```
   
4.  By default, your terminal remains attached to the container when you run `docker run`. 
    What if you don't want to remain attached?

    By adding the `-d` flag, we can run in detached mode, meaning the container will continue to run as long as the command is, 
    but it won't print the output.

    Let's run `/bin/sleep 3600`, which will run the container idly for 1 hour:

    ```
    $ docker run -d ubuntu:22.04 /bin/sleep 3600
      44c6bab63669624f080f4044e4a47465204c2351d46a1e8b5df0f255973eccb4
    $
    ```
    >:exclamation: **Wymagany screenshot 16!**

    If we check the container, we can see it's running the sleep command in a new container.

    ```
    $ docker ps
      CONTAINER ID   IMAGE          COMMAND             CREATED          STATUS          PORTS     NAMES
      9a14abef4c10   ubuntu:22.04   "/bin/sleep 3600"   46 minutes ago   Up 46 minutes             stupefied_germain
    $
    ```
    >:exclamation: **Wymagany screenshot 17!**

5. Now that the container is running in the background, what if we want to reattach to it?

    Maybe, if this were something like a web server or other process where we might like to inspect logs while it runs, 
    it'd be useful to run something on the container without interrupting the current process.
    To this end, there is another command, called `docker exec`. 
    `docker exec` runs a command within a container that is already running. 
    It works exactly like `docker run`, except instead of taking an image ID, it takes a container ID.
    This makes the `docker exec` command useful for tailing logs, or "SSHing" into an active container.

    Let's do that now, running the following, passing the first few characters of the container ID:

    ```
    artur@Artur-PC:~/Desktop/PROJECTS/materials-about-containerized-applications$ docker exec -it 9a1 /bin/bash
    root@9a14abef4c10:/# 

    ```
    >:exclamation: **Wymagany screenshot 18!**

    The container ID appearing at the front of the BASH prompt tells us we're inside the container. 
    Once inside a session, we can interact with the container like any SSH session.

    Let's list the running processes:

    ```
    root@9a14abef4c10:/# ps aux
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root           1  0.0  0.0   2792  1408 ?        Ss   11:10   0:00 /bin/sleep 3600
    root           7  0.0  0.0   4628  3328 pts/0    Ss   11:59   0:00 /bin/bash
    root          15  0.0  0.0   7064  2816 pts/0    R+   11:59   0:00 ps aux
    root@9a14abef4c10:/#
    ```
    >:exclamation: **Wymagany screenshot 19!**

    There we can see our running `/bin/sleep 3600` command. 
    Whenever we're done, we can type `exit` to exit our current BASH session, and leave the container running.

    ```
    root@9a14abef4c10:/# exit
    exit
    artur@Artur-PC:~/Desktop/PROJECTS/materials-about-containerized-applications$ sudo docker ps
    CONTAINER ID   IMAGE          COMMAND             CREATED          STATUS          PORTS     NAMES
    2041f1c61c29   ubuntu:22.04   "/bin/sleep 3600"   21 seconds ago   Up 21 seconds             cool_taussig
    ```
    >:exclamation: **Wymagany screenshot 20!**

    And finally checking `docker ps`, we can see the container is still running.

6. Instead of waiting 1 hour for this command to stop (and the container exit), what if we'd like to stop the Docker container now?

    To that end, we have the `docker stop` and the `docker kill` commands. The prior is a graceful stop, whereas the latter is a forceful one.

    Let's use `docker stop`, passing it the first few characters of the container name we want to stop.

    ```
    $ docker stop 2041
    2041
    ```
    >:exclamation: **Wymagany screenshot 21!**

    Then checking `docker ps -a`...

    ```
    $ docker ps -a
    CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS                        PORTS     NAMES
    2041f1c61c29   ubuntu:22.04   "/bin/sleep 3600"        2 minutes ago   Exited (137) 38 seconds ago             cool_taussig
    $
    ```
    >:exclamation: **Wymagany screenshot 22!**

    We can see that it exited with code `137`, which in Linux world means the command was likely aborted with a `kill -9` command.

### Removing containers

7. After working with Docker containers, you might want to delete old, obsolete ones.

    ```
    $ docker ps -a
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                        PORTS     NAMES
    2041f1c61c29   ubuntu:22.04   "/bin/sleep 3600"        19 minutes ago   Exited (137) 17 minutes ago             cool_taussig
    9a14abef4c10   ubuntu:22.04   "/bin/sleep 3600"        3 hours ago      Exited (0) 2 hours ago                  stupefied_germain
    a32fa5684874   ubuntu:22.04   "/bin/echo 'Hello wo…"   23 hours ago     Exited (0) 23 hours ago                 modest_bassi
    $
    ```
    >:exclamation: **Wymagany screenshot 23!**

    From our previous example, we can see with `docker ps -a` that we have a container hanging around.

    To remove this we can use the `docker rm` command which removes stopped containers.

    ```
    $ docker rm 2041
    2041
    ```

    A nice shortcut for removing all containers from your system is `docker rm $(docker ps -a -q)`:
    ```
   $ docker rm $(docker ps -a -q)
   9a14abef4c10
   a32fa5684874
   $ docker ps -a
   CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
   artur@Artur-PC:~/Desktop/PROJECTS/materials-about-containerized-applications$ 
   ```
    It can be tedious to remove old containers each time after you run them. 
    To address this, Docker also allows you to specify the `--rm` flag to the `docker run` command, 
    which will remove the container after it exits.

    ```
    $ docker run --rm ubuntu:22.04 /bin/echo 'Hello and goodbye!'
    Hello and goodbye!
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    $
    ```

# END OF EXERCISE 1