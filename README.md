Praise be to Allah

---
title: Abstract
...

Bluetooth is by nature a connection-oriented technology which provides a
master-slave structure between connected devices. In addition it
restricts the number of devices participating in the network to 7 in one
Piconet.

Thinking of ways to overcome Bluetooth limitations brought me to a
solution which provides a way to have a connectionless peer-to-peer
communication/data transfer among an unlimited number of devices.

The method, its implementation and necessary explanations are provided
during the following sections.

How Bluetooth works?

For two devices to communicate, they must get paired at the very
beginning. The following is how two Bluetooth devices start their
communication:

1.  The initiator device starts scanning the environment to look for the
    other one.

2.  The second device must announce its existence and the services
    it provides.

3.  The initiator device finds its target and the suitable service which
    is attached with information, including Name, Description, Protocol
    and the Port which the service is listening on.

4.  The initiator then opens a socket to the service. If the target
    device accepts, the connection is established.

For more clarity the following illustration is provided.

![](media/image5.png)![](media/image6.png)

This is the whole idea considering the initiator as the master and the
rest of devices as slaves with this in mind that only as small number of
devices as 7 can get involved.

How to bypass the limitations?

Now, I came up with an idea which makes it possible for Bluetooth
devices to communicate without getting paired or having any limit in the
number of devices participating in a network. It also exhibits a
peer-to-peer structure rather than a master-slave one. The following
describes the idea:

1.  Each device is consisted of a server thread and a client thread. The
    server thread starts advertising a specific service and the client
    thread starts scanning the environment for devices advertising that
    specific service.

2.  Each peer (device) sends its data to possible peers by placing the
    data it wants to share in the ‘description’ field of the service it
    is advertising (in its server thread).

3.  Furthermore each peer retrieves other peer’s data via scanning
    available devices in the range then fetching their services looking
    for that specific service advertised by other peers and finally
    retrieving the ‘description’ field of the service.

For more explanation the following illustration is provided.

Proof of Concept

To demonstrate the validity of the idea I wrote a public chat
application by Python programming language using PyBluez library (this
way, it can be used in all major operating systems). It turned out that
the idea works fine. Using two laptops I achieved the following result.
Program architecture, analysis and time complexity evaluations are
provided in the following sections.

![](media/image9.png)

Program’s Architecture

The Client part is a separate thread.

The Server part is an independent process.

The GUI is the main thread that enters GUI’s ‘mainloop’.

Time Complexity

The bottleneck lies in the Client thread which is consisted of 2 nested
loops. The outer loop iterates over found devices and the inner one
iterates over each device’s advertised services. The time grows as the
number of devices in the environment grows. I can’t tell yet whether the
order of the time growth is exponentially or not. But it took a
significant amount of time in an environment with some 24 discoverable
devices from which 3 laptops were running the intended software.
Unfortunately no accurate measurements are available.

The scanning phase has been implemented in a synchronous manner. I
suppose if this process happens asynchronously instead, we can achieve a
great speed up. Not to exaggerate, probably the speed up will be a
breakthrough indeed.

Pros & Cons

**Pros:**

1.  Providing a connectionless way of data transfer for Bluetooth
    technology which is a connection-oriented technology by nature.

2.  Providing a peer-to-peer network structure for Bluetooth technology
    which is by nature a master-slave technology.

3.  Involving an unlimited number of devices in the (If implemented,
    Bluetooth technology only supports 7 devices in one Piconet).

**Cons:**

1.  There is an inherent scanning time which can only be reduced,
    not eliminated.

2.  Available devices may be neglected time to time in searches. Highly
    depends on the device scanning accuracy.

3.  Time to update grows as the number of devices grow in the
    environment, however, it can be resolved by focusing on devices
    of interest.

Android App

Beside the desktop version which can be run on all major operating
systems I tried to write a similar App in Android OS. However I didn’t
make it due to limitations implied to Bluetooth APIs in handheld
devices, the result is an application which turns on the device’s
Bluetooth, scans the environment, then shows the result in a list
(unlike the desktop version, the process happens asynchronously here)
then turns off the Bluetooth on its exit.

There’s something called Gatt server introduced with Bluetooth Low
Energy which I believed can be used for the purpose. After working on
the idea, I couldn’t achieve anything. But yet, it seems to be a
potential solution.

![](media/image10.png)Extra Works

The code to discover Bluetooth devices around and retrieving their
services, opening a socket to a Bluetooth service and advertising a
service is also supplied with the project.
