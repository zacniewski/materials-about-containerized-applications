# Exercise 1: Running containers

In this exercise, we'll learn the basics of pulling images, starting, stopping, and removing containers.

### Pulling an image

To run containers, we'll first need to pull some images.

1. Let's see what images we have currently on our machine, by running `docker images`:

    ```
    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ```
    :exclamation: Wymagany screenshot!

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
3. We can also pull different versions on the same image.

    Run `docker pull ubuntu:22.10` to pull an image of Ubuntu 22.10.

    ```
    22.10: Pulling from library/ubuntu
    3ad6ea492c35: Pull complete 
    Digest: sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489
    Status: Downloaded newer image for ubuntu:22.10
    docker.io/library/ubuntu:22.10
    ```

    Potem, kiedy znów uruchomimy `docker images` znowu, powinniśmy dostać:

    ```
    REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
    ubuntu       22.04     53a843653cbc   4 weeks ago     77.9MB
    ubuntu       22.10     692eb4a905c0   14 months ago   70.3MB
    ```

4. Z biegiem czasu możemy zgromadzić zbierać wiele obrazów, więc dobrze jest usunąć te niechciane.
   Uruchom `docker rmi <IMAGE ID>`, aby np. usunąć obraz Ubuntu 22.10, z którego nie będziesz korzystać.

    ```
    $ docker rmi 692eb4a905c0
    Untagged: ubuntu:22.10
    Untagged: ubuntu@sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489
    Deleted: sha256:692eb4a905c074054e0a35d647671f0e32ed150d15b23fd7bc745cfb2fdeddbd
    Deleted: sha256:1e8bb0620308641104e68d66f65c1e51de68d7df7240b8a99a251338631c6911
    ```

    Alternatywnie możesz usunąć obrazy po tagu lub za pomocą częściowego identyfikatora obrazu. 
    Dla poprzedniego przykładu, poniższe komendy byłyby równoważne:  
     - `docker rmi 69`
     - `docker rmi ubuntu:22.10`

    Uruchomienie `docker images` powinno odzwierciedlić zmiany po usuniętym obrazie.

    ```
    $ docker images
    REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
    ubuntu       22.04     53a843653cbc   4 weeks ago   77.9MB
    ```

    Skrót do usuwania wszystkich obrazów z systemu to `docker rmi $(docker images -a -q)`
    ```
    $ docker rmi $(docker images -a -q)
    Untagged: ubuntu:22.04
    Untagged: ubuntu@sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658
    Deleted: sha256:53a843653cbcd9e10be207e951d907dc2481d9c222de57d24cfcac32e5165188
    Deleted: sha256:1b9b7346fee7abbc7f5538eaa23548bd05a45abe8daf6794024be0c8ad7d60bb
    ```

### Uruchamianie kontenera

Korzystając z pobranego przez nas obrazu Ubuntu 22.04, możemy uruchomić nasz pierwszy kontener. 
W przeciwieństwie do tradycyjnego frameworka wirtualizacji, takiego jak VirtualBox czy VMWare, nie możemy po prostu uruchomić maszyny wirtualnej z systemem uruchamianym tym obrazem bez niczego innego: musimy dać mu polecenie uruchomienia.
Polecenie może być wszystkim, co chcesz, o ile istnieje w pobranym obrazie. 
W przypadku obrazu Ubuntu jest to jądro Linuksa z wieloma typowymi aplikacjami, które można znaleźć w podstawowym środowisku Linux.

1.  Zróbmy bardzo prosty przykład. Uruchom `docker run ubuntu:22.04 /bin/echo 'Hello world!'`
    Jeśli usunęliśmy obraz wcześniej, to zostanie on na nowo pobrany

    ```
    $ docker run ubuntu:22.04 /bin/echo 'Hello world!'
    Unable to find image 'ubuntu:22.04' locally
    22.04: Pulling from library/ubuntu
    857cc8cb19c0: Pull complete 
    Digest: sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658
    Status: Downloaded newer image for ubuntu:22.04
    Hello world!
    ```

    The `/bin/echo` command is a really simple application that just prints whatever you give it to the terminal. We passed it 'Hello world!', so it prints `Hello world!` to the terminal.

    When you run the whole `docker run` command, it creates a new container from the image specified, then runs the command inside the container. From the previous example, the Docker container started, then ran the `/bin/echo` command in the container.

2. Let's check what containers we have after running this. Run `docker ps`

    ```
    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    ```

    That's strange: no containers right? The `ps` command doesn't show stopped containers by default, add the `-a` flag.

    ```
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS                          PORTS               NAMES
    4fc37e27944a        ubuntu:16.04        "/bin/echo 'Hello ..."   About a minute ago   Exited (0) About a minute ago                       zen_swartz
    ```

    Okay, there's our container. But why is the status "Exited"?

    *Docker containers only run as long as the command it starts with is running.* In our example, it ran `/bin/echo` successfully, printed some output, then exited with status code 0 (which means no errors.) When Docker saw this command exit, the container stopped.

3. Let's do something a bit more interactive. Run `docker run ubuntu:16.04 /bin/bash`

    ```
    $ docker run ubuntu:16.04 /bin/bash
    $
    ```

    Notice nothing happened. When we run `docker ps -a`

    ```
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
    654792eb403b        ubuntu:16.04        "/bin/bash"         4 seconds ago       Exited (0) 2 seconds ago                       distracted_minsky
    ```

    The container exited instantly. Why? We were running the `/bin/bash` command, which is an interactive program. However, the `docker run` command doesn't run interactively by default, therefore the `/bin/bash` command exited, and the container stopped.

    Instead, let's add the `-it` flags, which tells Docker to run the command interactively with your terminal.

    ```
    $ docker run -it ubuntu:16.04 /bin/bash
    root@5fa68739793c:/# 
    ```

    This looks a lot better. This means you're in a BASH session inside the Ubuntu container. Notice you're running as `root` and the container ID that follows.

    You can now use this like a normal Linux shell. Try `pwd` and `ls` to look at the file system.

    ```
    root@5fa68739793c:/# pwd
    /
    root@5fa68739793c:/# ls
    bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
    ```

    You can type `exit` to end the BASH session, terminating the command and stopping the container.

    ```
    root@5fa68739793c:/# exit
    exit
    $
    ```
4. By default your terminal remains attached to the container when you run `docker run`. What if you don't want to remain attached?

    By adding the `-d` flag, we can run in detached mode, meaning the container will continue to run as long as the command is, but it won't print the output.

    Let's run `/bin/sleep 3600`, which will run the container idly for 1 hour:

    ```
    $ docker run -d ubuntu:16.04 /bin/sleep 3600
    be730b8c554b69383f30f71222b9ac264367c7454790dc2a4eb0cda33c0baa2a
    $
    ```

    If we check the container, we can see it's running the sleep command in a new container.

    ```
    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    be730b8c554b        ubuntu:16.04        "/bin/sleep 3600"    41 seconds ago      Up 40 seconds                           jovial_goldstine
    $
    ```

5. Now that the container is running in the background, what if we want to reattach to it?

    Conceivably, if this were something like a web server or other process where we might like to inspect logs while it runs, it'd be useful to run something on the container without interrupting the current process.

    To this end, there is another command, called `docker exec`. `docker exec` runs a command within a container that is already running. It works exactly like `docker run`, except instead of taking an image ID, it takes a container ID.

    This makes the `docker exec` command useful for tailing logs, or "SSHing" into an active container.

    Let's do that now, running the following, passing the first few characters of the container ID:

    ```
    $ docker exec -it be7 /bin/bash
    root@be730b8c554b:/#
    ```

    The container ID appearing at the front of the BASH prompt tells us we're inside the container. Once inside a session, we can interact with the container like any SSH session.

    Let's list the running processes:

    ```
    root@be730b8c554b:/# ps aux
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root         1  0.2  0.0   4380   796 ?        Ss   15:41   0:00 /bin/sleep 3600
    root         6  0.6  0.1  18240  3208 ?        Ss   15:41   0:00 /bin/bash
    root        16  0.0  0.1  34424  2808 ?        R+   15:41   0:00 ps aux
    root@be730b8c554b:/#
    ```

    There we can see our running `/bin/sleep 3600` command. Whenever we're done, we can type `exit` to exit our current BASH session, and leave the container running.

    ```
    root@be730b8c554b:/# exit
    exit
    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    be730b8c554b        ubuntu:16.04        "/bin/sleep 3600"   9 minutes ago       Up 9 minutes                            jovial_goldstine
    $
    ```

    And finally checking `docker ps`, we can see the container is still running.

6. Instead of waiting 1 hour for this command to stop (and the container exit), what if we'd like to stop the Docker container now?

    To that end, we have the `docker stop` and the `docker kill` commands. The prior is a graceful stop, whereas the latter is a forceful one.

    Let's use `docker stop`, passing it the first few characters of the container name we want to stop.

    ```
    $ docker stop be73
    be73
    ```

    Then checking `docker ps -a`...

    ```
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
    be730b8c554b        ubuntu:16.04        "/bin/sleep 600"         1 minute ago        Exited (137) 1 minute ago                       jovial_goldstine
    $
    ```

    We can see that it exited with code `137`, which in Linux world means the command was likely aborted with a `kill -9` command.

### Removing containers

7. After working with Docker containers, you might want to delete old, obsolete ones.

    ```
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS               NAMES
    be730b8c554b        ubuntu:16.04        "/bin/sleep 600"         1 minute ago        Exited (137) 1 minute ago                       jovial_goldstine
    $
    ```

    From our previous example, we can see with `docker ps -a` that we have a container hanging around.

    To remove this we can use the `docker rm` command which removes stopped containers.

    ```
    $ docker rm be73
    be73
    ```

    A nice shortcut for removing all containers from your system is `docker rm $(docker ps -a -q)`

    It can be tedious to remove old containers each time after you run them. To address this, Docker also allows you to specify the `--rm` flag to the `docker run` command, which will remove the container after it exits.

    ```
    $ docker run --rm ubuntu:16.04 /bin/echo 'Hello and goodbye!'
    Hello and goodbye!
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    $
    ```

# END OF EXERCISE 1