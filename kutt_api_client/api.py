#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Modules
"""
import requests
from typing import Optional
from .models import (
    Link,
    Stats,
    CreateLinkRequest,
    UpdateLinkRequest,
    DeleteResponse,
    LinkListResponse,
    GetLinksRequest,
)


class KuttAPI:
    def __init__(self, api_key: str, base_url: str = "https://kutt.it/api/v2"):
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": api_key
            # "Content-Type": "application/json"
        }

    def create_link(self, payload: CreateLinkRequest) -> Link:
        response = requests.post(
            f"{self.base_url}/links", headers=self.headers, json=payload.dump_kutt()
        )
        response.raise_for_status()
        return Link(**response.json())

    def update_link(self, payload: UpdateLinkRequest) -> Link:
        response = requests.patch(
            f"{self.base_url}/links/{str(payload.id)}", headers=self.headers, json=payload.dump_kutt()
        )
        response.raise_for_status()
        return Link(**response.json())

    def get_links(self, request: Optional[GetLinksRequest] = None) -> LinkListResponse:
        """
        Holt alle Links von Kutt, auch wenn die API maximal 50 pro Request zurückliefert.
        Nutzt eine Schleife, um alle Seiten abzufragen.
        """
        if request is None:
            request = GetLinksRequest()

        all_links: List[Link] = []
        skip = request.skip

        while True:
            # Nutze dump_kutt, aber überschreibe skip dynamisch
            params = request.dump_kutt()
            params['skip'] = skip
            response = requests.get(f"{self.base_url}/links", headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json().get('data', [])
            if not data:  # Abbruch, wenn keine Links mehr kommen
                break

            # Alle Links in Pydantic-Objekte umwandeln
            all_links.extend([Link(**item) for item in data])

            # Kutt liefert max. 50, daher skip erhöhen
            skip += len(data)

        return LinkListResponse(
            limit=len(all_links),
            skip=request.skip,
            total=len(all_links),
            data=all_links
        )

    def delete_link(self, link_id: str) -> DeleteResponse:
        response = requests.delete(f"{self.base_url}/links/{link_id}", headers=self.headers)
        response.raise_for_status()
        return DeleteResponse(**response.json())

    def get_link_stats(self, link_id: str) -> Stats:
        response = requests.get(f"{self.base_url}/links/{link_id}/stats", headers=self.headers)
        response.raise_for_status()
        return Stats(**response.json())
