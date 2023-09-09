# Project Edna: Enabling Connectionless Peer-to-Peer Data Transfer via Bluetooth

Bluetooth technology, inherently reliant on a connection-oriented paradigm and imposing a strict limit of seven devices within a single Piconet, presents certain limitations. This project endeavors to overcome these constraints by introducing an innovative approach that enables connectionless peer-to-peer communication and data transfer, effectively allowing an unlimited number of devices to participate. This README provides a comprehensive overview of this novel method, its implementation, and detailed explanations.

## Table of Contents

- [Traditional Bluetooth Communication](#traditional-bluetooth-communication)
- [An Innovative Approach: Connectionless Peer-to-Peer Communication](#an-innovative-approach-connectionless-peer-to-peer-communication)
- [Proof of Concept: Public Chat Application](#proof-of-concept-public-chat-application)
- [Program Architecture](#program-architecture)
- [Time Complexity](#time-complexity)
- [Pros and Cons](#pros-and-cons)

## Traditional Bluetooth Communication

In conventional Bluetooth communication, two devices initiate interaction through a pairing process:

1. **Device Discovery**: The initiator device scans its surroundings to detect other devices.
2. **Device Advertisement**: The second device broadcasts its presence and the services it offers.
3. **Target Selection**: The initiator device identifies its target and the suitable service, encompassing Name, Description, Protocol, and Port.
4. **Connection Establishment**: Subsequently, the initiator establishes a connection to the service, and if the target device accepts, the connection is established.

![Bluetooth Communication](/media/image1.png)

This conventional approach designates one device as the master and the rest as slaves, with a strict limitation of only seven devices permitted to participate.

## An Innovative Approach: Connectionless Peer-to-Peer Communication

To circumvent these limitations and empower Bluetooth devices to communicate without the need for pairing and without imposing constraints on the number of participating devices, we propose a peer-to-peer structure:

1. **Server and Client Threads**: Each device is equipped with a server thread and a client thread. The server thread advertises a specific service, while the client thread scans the environment for devices advertising that service.
2. **Data Sharing**: Peers share data with one another by embedding the data they wish to transmit in the 'description' field of the service they are advertising.
3. **Data Retrieval**: Devices retrieve data from other peers by scanning available devices, inspecting their services for the specific service advertised by fellow peers, and retrieving the data from the 'description' field.

![Peer-to-Peer Bluetooth](/media/image2.png)

## Proof of Concept: Public Chat Application

To validate this concept, a public chat application was developed using Python and the PyBluez library. This application effectively demonstrated peer-to-peer communication using two laptops.

![Chat Application](/media/image3.png)

## Program Architecture

The program architecture is structured as follows:

- **Client Component**: Operating as a separate thread.
- **Server Component**: Functioning as an independent process.
- **Graphical User Interface (GUI)**: Managed by the main thread, which enters the GUI's 'mainloop'.

![Program Architecture](/media/image4.png)

## Time Complexity

The time complexity primarily hinges on the client thread, comprising nested loops. The outer loop iterates over discovered devices, while the inner loop iterates over each device's advertised services. As the number of devices in the environment increases, the time required also scales. Further analysis is warranted to ascertain the precise order of time growth, as accurate measurements remain pending.

The current synchronous implementation of the scanning phase leaves room for improvement. Implementing an asynchronous approach holds promise for potentially significant speed enhancements.

## Pros and Cons

**Pros:**

1. Pioneers a connectionless method for data transfer in Bluetooth, addressing a technology inherently designed around connections.
2. Transforms Bluetooth from a master-slave structure into a peer-to-peer network, thereby expanding its utility.
3. Eliminates the restriction on the number of devices, permitting an unlimited number of devices to participate, in stark contrast to Bluetooth's traditional seven-device limit within one Piconet.

**Cons:**

1. The inherent scanning time, while reducible, remains a factor.
2. Occasional oversights of available devices during scans may occur, contingent on scanning accuracy.
3. As the number of devices in the environment grows, update times increase, potentially mitigated through focused attention on devices of interest.
