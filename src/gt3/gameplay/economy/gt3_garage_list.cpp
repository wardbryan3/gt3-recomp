// Memory-native projections of original unit 004F.cpp (lines 756 and 825),
// not full ABI. 32-bit guest addresses; +4u additions wrap. Insertion does
// not initialize node+4, and the empty-list branch does not write node's
// next link: callers must supply a detached node.
#include "gt3_garage.hpp"

namespace gt3::economy_recovery {

// 004F.cpp:756 — insert `node` at the collection head (list = head ptr,
// list+4 = tail ptr; record links: node = next, node+4 = prev).
std::uint32_t FUN_0023c1b8(garage_memory& m, std::uint32_t list, std::uint32_t node) {
    if (node == 0u) {
        return list;
    }
    std::uint32_t head = m.load32(list);
    if (head == 0u) {
        m.store32(list + 4u, node);
    } else {
        m.store32(head + 4u, node);
        head = m.load32(list); // exact original sequence: reload after store
        m.store32(node, head);
    }
    m.store32(list, node);
    return list;
}

// 004F.cpp:825 — unlink `node` from the collection. Each comparison re-reads
// memory in the exact original order; no load is cached across a store.
std::uint32_t FUN_0023c288(garage_memory& m, std::uint32_t list, std::uint32_t node) {
    if (node == 0u) {
        return list;
    }
    if (node == m.load32(list)) {
        m.store32(list, m.load32(node));
    }
    if (node == m.load32(list + 4u)) {
        m.store32(list + 4u, m.load32(node + 4u));
    }
    const std::uint32_t next = m.load32(node);
    if (next != 0u) {
        m.store32(next + 4u, m.load32(node + 4u));
    }
    const std::uint32_t prev = m.load32(node + 4u);
    if (prev != 0u) {
        m.store32(prev, m.load32(node));
    }
    m.store32(node + 4u, 0u);
    m.store32(node, 0u);
    return list;
}

}
