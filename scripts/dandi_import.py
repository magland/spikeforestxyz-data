import os
import dandi.dandiarchive as da
import datalad.api as dl


def dandi_import():
    dandiset_id = '000871'  # https://neurosift.app/?p=/dandiset&dandisetId=000618&dandisetVersion=draft
    dandiset_version = 'draft'
    dendro_project_id = '9e302504'  # https://dendro.vercel.app/project/9e302504?tab=project-home

    parsed_url = da.parse_dandi_url(f"https://dandiarchive.org/dandiset/{dandiset_id}")

    with parsed_url.navigate() as (client, dandiset, assets):
        if dandiset is None:
            print(f"Dandiset {dandiset_id} not found.")
            return
        for asset_obj in dandiset.get_assets('path'):
            if not asset_obj.path.endswith(".nwb"):
                continue
            print(asset_obj.path)
            print('=====================')

            output_path = f'data/recordings/{asset_obj.path}'
            if os.path.exists(output_path):
                print("Skipping - already exists")
                continue
            dl.run(
                f'spikeforestxyz import-dandi-nwb --dandiset-id {dandiset_id} --dandiset-version {dandiset_version} --nwb-file-url {asset_obj.path} --nwb-file-path {asset_obj.path} --output-path {output_path}',
                outputs=[output_path]
            )


if __name__ == '__main__':
    dandi_import()
